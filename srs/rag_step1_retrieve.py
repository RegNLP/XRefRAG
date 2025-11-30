#!/usr/bin/env python
"""
RAG Step 1: Retrieval

Given:
  - full passages file (JSONL)
  - final test set (JSONL)
  - retriever name (bm25, e5, bge, bm25_e5_rerank, hybrid_rrf_bm25_e5)

Produces:
  - retrieval JSONL with one line per QA:
      {
        "qa_id": "DPEL_000677",
        "retriever": "hybrid_rrf_bm25_e5",
        "question": "...",
        "retrieved": [
          {"pid": "...", "rank": 1, "score": 0.123},
          ...
        ]
      }
"""

import argparse
import json
import os
from collections import defaultdict
from typing import Dict, List, Tuple

import numpy as np
from tqdm import tqdm

# BM25 (Pyserini)
from pyserini.search.lucene import LuceneSearcher

# Dense retrievers
from sentence_transformers import SentenceTransformer


# ------------------------------------------------------------------
# Utilities
# ------------------------------------------------------------------


def load_passages(path: str) -> Dict[str, str]:
    """
    Load passages_full.jsonl into a dict: pid -> text

    We try several common field names to be robust:
      - id / pid / passage_id
      - text / passage / passage_text
    """
    passages: Dict[str, str] = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            pid = str(
                obj.get("pid")
                or obj.get("id")
                or obj.get("passage_id")
                or obj.get("PassageID")
            )
            text = (
                obj.get("text")
                or obj.get("passage")
                or obj.get("passage_text")
                or obj.get("Passage")
            )
            if pid and text:
                passages[pid] = text
    if not passages:
        raise ValueError(f"No passages loaded from {path}")
    print(f"[INFO] Loaded {len(passages)} passages from {path}")
    return passages


def load_test_items(path: str) -> List[Dict[str, str]]:
    """
    Load final test.jsonl and extract (qa_id, question) for each item.

    Example item (your DPEL/SCHEMA test line):
      {
        "persona": "Professional",
        "question": "...",
        "answer": "...",
        "source_passage_id": "...",
        "target_passage_id": "...",
        ...
        "id": "DPEL_000677",
        "method": "DPEL",
        "split": "test"
      }

    We use:
      qid = id / qa_id / QuestionID / line index
      question = question / Question
    """
    items: List[Dict[str, str]] = []
    with open(path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            qid = str(
                obj.get("id")
                or obj.get("qa_id")
                or obj.get("QuestionID")
                or idx
            )
            qtext = obj.get("question") or obj.get("Question")
            if not qtext:
                # Skip weird lines
                continue
            items.append({"qa_id": qid, "question": qtext})
    if not items:
        raise ValueError(f"No test items loaded from {path}")
    print(f"[INFO] Loaded {len(items)} test items from {path}")
    return items


# ------------------------------------------------------------------
# Retriever implementations
# ------------------------------------------------------------------


class BM25Retriever:
    def __init__(self, index_dir: str, k1: float = 0.9, b: float = 0.4):
        if not os.path.isdir(index_dir):
            raise ValueError(f"BM25 index dir not found: {index_dir}")
        self.searcher = LuceneSearcher(index_dir)
        self.searcher.set_bm25(k1=k1, b=b)

    def retrieve(self, query: str, k: int) -> List[Tuple[str, float]]:
        hits = self.searcher.search(query, k=k)
        return [(h.docid, float(h.score)) for h in hits]


class DenseRetriever:
    """
    Generic dense retriever with SentenceTransformers.

    Supports query / passage prefixes (e.g. for e5, bge).
    """

    def __init__(
        self,
        passages: Dict[str, str],
        model_name: str,
        query_prefix: str = "",
        passage_prefix: str = "",
        batch_size: int = 64,
    ):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.query_prefix = query_prefix
        self.passage_prefix = passage_prefix

        self.pids: List[str] = list(passages.keys())
        texts = [self.passage_prefix + passages[pid] for pid in self.pids]

        print(f"[DenseRetriever] Encoding {len(self.pids)} passages with {model_name}...")
        self.embs = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

    def retrieve(self, query: str, k: int) -> List[Tuple[str, float]]:
        q_emb = self.model.encode(
            [self.query_prefix + query],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )[0]
        scores = np.dot(self.embs, q_emb)
        k = min(k, len(self.pids))
        idx = np.argpartition(-scores, k - 1)[:k]
        idx = idx[np.argsort(-scores[idx])]
        return [(self.pids[i], float(scores[i])) for i in idx]


class BM25E5RerankRetriever:
    """
    1) BM25 to get candidate set
    2) Re-rank candidates with E5 dense model
    """

    def __init__(self, bm25: BM25Retriever, dense: DenseRetriever, candidate_k: int = 50):
        self.bm25 = bm25
        self.dense = dense
        self.candidate_k = candidate_k

        # Build a small lookup from pid -> row index in dense.embs
        self.pid_to_idx = {pid: i for i, pid in enumerate(self.dense.pids)}

    def retrieve(self, query: str, k: int) -> List[Tuple[str, float]]:
        bm25_hits = self.bm25.retrieve(query, k=self.candidate_k)
        candidate_pids = [pid for pid, _ in bm25_hits]

        # Encode query once
        q_emb = self.dense.model.encode(
            [self.dense.query_prefix + query],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )[0]

        scores = []
        for pid in candidate_pids:
            idx = self.pid_to_idx.get(pid)
            if idx is None:
                continue
            score = float(np.dot(self.dense.embs[idx], q_emb))
            scores.append((pid, score))

        # Sort by dense score
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:k]


class HybridRRFRetriever:
    """
    RRF fusion of BM25 and Dense retriever (e5).

    1) Get topK from BM25
    2) Get topK from Dense (e5)
    3) Combine with RRF
    """

    def __init__(self, bm25: BM25Retriever, dense: DenseRetriever, rrf_k: int = 60):
        self.bm25 = bm25
        self.dense = dense
        self.rrf_k = rrf_k

    def _rrf_fuse(
        self,
        bm25_hits: List[Tuple[str, float]],
        dense_hits: List[Tuple[str, float]],
        k: int,
    ) -> List[Tuple[str, float]]:
        scores = defaultdict(float)

        for rank, (pid, _) in enumerate(bm25_hits, start=1):
            scores[pid] += 1.0 / (self.rrf_k + rank)

        for rank, (pid, _) in enumerate(dense_hits, start=1):
            scores[pid] += 1.0 / (self.rrf_k + rank)

        # sort by fused score
        sorted_items = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_items[:k]

    def retrieve(self, query: str, k: int) -> List[Tuple[str, float]]:
        bm25_hits = self.bm25.retrieve(query, k=k)
        dense_hits = self.dense.retrieve(query, k=k)
        return self._rrf_fuse(bm25_hits, dense_hits, k=k)


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--passages",
        required=True,
        help="Path to passages_full.jsonl",
    )
    parser.add_argument(
        "--test-json",
        required=True,
        help="Path to final test.jsonl (DPEL/SCHEMA)",
    )
    parser.add_argument(
        "--retriever",
        required=True,
        choices=["bm25", "e5", "bge", "bm25_e5_rerank", "hybrid_rrf_bm25_e5"],
        help="Retriever type",
    )
    parser.add_argument(
        "--bm25-index",
        help="Path to BM25 (Pyserini) index dir (required for bm25, bm25_e5_rerank, hybrid_rrf_bm25_e5)",
    )
    parser.add_argument(
        "--topk",
        type=int,
        default=50,
        help="Number of passages to retrieve per query",
    )
    parser.add_argument(
        "--out-jsonl",
        required=True,
        help="Output JSONL file with retrieval results",
    )

    args = parser.parse_args()

    # Load data
    passages = load_passages(args.passages)
    test_items = load_test_items(args.test_json)

    # Initialise retriever
    retriever_obj = None

    if args.retriever == "bm25":
        if not args.bm25_index:
            raise ValueError("--bm25-index is required for bm25 retriever")
        retriever_obj = BM25Retriever(args.bm25_index)

    elif args.retriever == "e5":
        retriever_obj = DenseRetriever(
            passages,
            model_name="intfloat/e5-base-v2",
            query_prefix="query: ",
            passage_prefix="passage: ",
        )

    elif args.retriever == "bge":
        retriever_obj = DenseRetriever(
            passages,
            model_name="BAAI/bge-base-en-v1.5",
            query_prefix="query: ",
            passage_prefix="passage: ",
        )

    elif args.retriever == "bm25_e5_rerank":
        if not args.bm25_index:
            raise ValueError("--bm25-index is required for bm25_e5_rerank retriever")
        bm25 = BM25Retriever(args.bm25_index)
        dense = DenseRetriever(
            passages,
            model_name="intfloat/e5-base-v2",
            query_prefix="query: ",
            passage_prefix="passage: ",
        )
        retriever_obj = BM25E5RerankRetriever(bm25=bm25, dense=dense, candidate_k=args.topk)

    elif args.retriever == "hybrid_rrf_bm25_e5":
        if not args.bm25_index:
            raise ValueError("--bm25-index is required for hybrid_rrf_bm25_e5 retriever")
        bm25 = BM25Retriever(args.bm25_index)
        dense = DenseRetriever(
            passages,
            model_name="intfloat/e5-base-v2",
            query_prefix="query: ",
            passage_prefix="passage: ",
        )
        retriever_obj = HybridRRFRetriever(bm25=bm25, dense=dense)

    else:
        raise ValueError(f"Unknown retriever: {args.retriever}")

    # Run retrieval and write JSONL
    os.makedirs(os.path.dirname(args.out_jsonl), exist_ok=True)
    n_queries = 0

    with open(args.out_jsonl, "w", encoding="utf-8") as out_f:
        for item in tqdm(test_items, desc=f"Retrieving with {args.retriever}"):
            qa_id = item["qa_id"]
            question = item["question"]

            hits = retriever_obj.retrieve(question, k=args.topk)

            record = {
                "qa_id": qa_id,
                "retriever": args.retriever,
                "question": question,
                "retrieved": [
                    {"pid": pid, "rank": rank, "score": score}
                    for rank, (pid, score) in enumerate(hits, start=1)
                ],
            }
            out_f.write(json.dumps(record) + "\n")
            n_queries += 1

    print(f"[INFO] Wrote retrieval results for {n_queries} queries to {args.out_jsonl}")


if __name__ == "__main__":
    main()
