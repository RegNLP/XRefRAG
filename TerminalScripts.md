cd /Users/tuba.gokhan/Documents/GitHub/RegRAG-Xref

export OPENAI_API_KEY=""

python srs/extract_schemas.py \
  --input_csv data/CrossReferenceData.csv \
  --output_jsonl outputs/extracted_schema.jsonl \
  --model gpt-4o \
  --drop_title_targets




# DPEL full and # SCHEMA full (uses outputs/extracted_schema.jsonl from step-1)
mkdir -p outputs/generation/dpel/all
mkdir -p outputs/generation/schema/all

python3 srs/generate_qas_method_DPEL.py \
  --input_csv data/CrossReferenceData.csv \
  --output_jsonl outputs/generation/dpel/all/answers.jsonl \
  --report_json outputs/generation/dpel/all/report.json \
  --model gpt-4o \
  --max_q_per_pair 2 \
  --sample_n 3 \
  --temperature 0.2 \
  --seed 13 \
  --dedup \
  --verbose
python srs/generate_qas_method_schema.py \
  --input_jsonl outputs/extracted_schema.jsonl \
  --output_jsonl outputs/generation/schema/all/answers.jsonl \
  --report_json outputs/generation/schema/all/report.json \
  --model gpt-4o \
  --max_q_per_pair 2 \
  --sample_n 3 \
  --temperature 0.2 \
  --seed 13 \
  --dual_anchors_mode freeform_only \
  --no_citations \
  --dedup \
  --verbose

python srs/inspect_qas_stats.py \
  --inputs outputs/generation/dpel/all/answers.jsonl \
           outputs/generation/schema/all/answers.jsonl \
  --out_csv outputs/generation/qa_stats_summary.csv \
  --sample 5

mkdir -p outputs/judging/ensemble

python srs/judge_qas_ensemble.py \
  --inputs outputs/generation/dpel/all/answers.jsonl \
           outputs/generation/schema/all/answers.jsonl \
  --out_jsonl outputs/judging/ensemble/judgments.jsonl \
  --report_json outputs/judging/ensemble/summary.json \
  --ensemble_models gpt-4.1-mini,gpt-4o-mini \
  --repeat_first_with_seed 17 \
  --pass_threshold 7 \
  --require_dual_use_k 2 \
  --forbid_citations_in_question_for_schema \
  --temperature 0.0 \
  --seed 13 \
  --verbose

mkdir -p outputs/judging/analysis

python srs/analyze_judgment_stats.py \
  --judgments outputs/judging/ensemble/judgments.jsonl \
  --gen_inputs outputs/generation/dpel/all/answers.jsonl \
               outputs/generation/schema/all/answers.jsonl \
  --out_dir outputs/judging/analysis


mkdir -p outputs/judging/curated

python srs/curate_from_judgments.py \
  --judgments outputs/judging/ensemble/judgments.jsonl \
  --gen_inputs outputs/generation/dpel/all/answers.jsonl \
               outputs/generation/schema/all/answers.jsonl \
  --out_dir outputs/judging/curated \
  --include_judge_payload \
  --verbose

mkdir -p data/ir inputs/ir runs/kept runs/eliminated indexes passages_json outputs/judging/analysis


python srs/build_ir_inputs.py \
  --inputs outputs/judging/curated/DPEL/kept.jsonl \
           outputs/judging/curated/DPEL/eliminated.jsonl \
           outputs/judging/curated/SCHEMA/kept.jsonl \
           outputs/judging/curated/SCHEMA/eliminated.jsonl
-----
# Pyserini
conda create -n regrag_xref python=3.11 -y
conda activate regrag_xref


# macOS ise:
brew install --cask temurin@21

export JAVA_HOME=$(/usr/libexec/java_home -v 21)
export PATH="$JAVA_HOME/bin:$PATH"
java -version   

pip install --upgrade pip
pip install 'pyserini[optional]'
pip install faiss-cpu pytrec_eval

------------
# IR

python -m pyserini.index.lucene \
  --collection JsonCollection \
  --input passages_json \
  --index indexes/bm25_full \
  --generator DefaultLuceneDocumentGenerator \
  --threads 4 \
  --storePositions --storeDocvectors --storeRaw


## BM25


python -m pyserini.search.lucene \
  --index indexes/bm25_full \
  --topics inputs/ir/queries_kept.tsv \
  --bm25 --k1 0.9 --b 0.4 \
  --hits 100 \
  --batch-size 64 --threads 4 \
  --output runs_full/kept/bm25.txt

python -m pyserini.search.lucene \
  --index indexes/bm25_full \
  --topics inputs/ir/queries_eliminated.tsv \
  --bm25 --k1 0.9 --b 0.4 \
  --hits 100 \
  --batch-size 64 --threads 4 \
  --output runs_full/eliminated/bm25.txt


-----
conda create -n e5_cpu python=3.10 -y
conda activate e5_cpu

conda install pytorch cpuonly -c pytorch -c conda-forge

pip install sentence-transformers faiss-cpu tqdm

# e5
python srs/run_dense_e5_sbert.py \
  --passages data/passages_full.jsonl \
  --model-name intfloat/e5-base-v2 \
  --queries inputs/ir/queries_kept.tsv \
  --output runs_full/kept/e5.txt \
  --k 100

python srs/run_dense_e5_sbert.py \
  --passages data/passages_full.jsonl \
  --model-name intfloat/e5-base-v2 \
  --queries inputs/ir/queries_eliminated.tsv \
  --output runs_full/eliminated/e5.txt \
  --k 100


#BGE:
python srs/run_dense_e5_sbert.py \
  --passages data/passages_full.jsonl \
  --model-name BAAI/bge-base-en-v1.5 \
  --queries inputs/ir/queries_kept.tsv \
  --output runs_full/kept/bge.txt \
  --k 100


python srs/run_dense_e5_sbert.py \
  --passages data/passages_full.jsonl \
  --model-name BAAI/bge-base-en-v1.5 \
  --queries inputs/ir/queries_eliminated.tsv \
  --output runs_full/eliminated/bge.txt \
  --k 100

# rerank

python srs/rerank_bm25_with_e5.py \
  --passages data/passages_full.jsonl \
  --queries inputs/ir/queries_kept.tsv \
  --bm25 runs_full/kept/bm25.txt \
  --output runs_full/kept/bm25_e5_rerank.txt \
  --model-name intfloat/e5-base-v2 \
  --k-candidate 200 \
  --k-output 100

python srs/rerank_bm25_with_e5.py \
  --passages data/passages_full.jsonl \
  --queries inputs/ir/queries_eliminated.tsv \
  --bm25 runs_full/eliminated/bm25.txt \
  --output runs_full/eliminated/bm25_e5_rerank.txt \
  --model-name intfloat/e5-base-v2 \
  --k-candidate 200 \
  --k-output 100


#Hybrid RRF (BM25_full + e5_full):

conda activate regrag_xref  

python srs/fuse_rrf.py \
  --bm25 runs_full/kept/bm25.txt \
  --dense runs_full/kept/e5.txt \
  --output runs_full/kept/hybrid_rrf_bm25_e5.txt \
  --k 100 --rrf-k 60

python srs/fuse_rrf.py \
  --bm25 runs_full/eliminated/bm25.txt \
  --dense runs_full/eliminated/e5.txt \
  --output runs_full/eliminated/hybrid_rrf_bm25_e5.txt \
  --k 100 --rrf-k 60

# EVAL
python srs/build_method_qrels.py \
  --dpel-kept outputs/judging/curated/DPEL/kept.jsonl \
  --dpel-elim outputs/judging/curated/DPEL/eliminated.jsonl \
  --schema-kept outputs/judging/curated/SCHEMA/kept.jsonl \
  --schema-elim outputs/judging/curated/SCHEMA/eliminated.jsonl

# ==== FULL CORPUS EVAL (runs_full) ====

python srs/eval_ir.py \
  --qrels inputs/ir/qrels_kept_dpel.txt \
  --runs \
    runs_full/kept/bm25.txt \
    runs_full/kept/bge.txt \
    runs_full/kept/e5.txt \
    runs_full/kept/bm25_e5_rerank.txt \
    runs_full/kept/hybrid_rrf_bm25_e5.txt \
  --k 10

python srs/eval_ir.py \
  --qrels inputs/ir/qrels_eliminated_dpel.txt \
  --runs \
    runs_full/eliminated/bm25.txt \
    runs_full/eliminated/bge.txt \
    runs_full/eliminated/e5.txt \
    runs_full/eliminated/bm25_e5_rerank.txt \
    runs_full/eliminated/hybrid_rrf_bm25_e5.txt \
  --k 10

python srs/eval_ir.py \
  --qrels inputs/ir/qrels_kept_schema.txt \
  --runs \
    runs_full/kept/bm25.txt \
    runs_full/kept/bge.txt \
    runs_full/kept/e5.txt \
    runs_full/kept/bm25_e5_rerank.txt \
    runs_full/kept/hybrid_rrf_bm25_e5.txt \
  --k 10

python srs/eval_ir.py \
  --qrels inputs/ir/qrels_eliminated_schema.txt \
  --runs \
    runs_full/eliminated/bm25.txt \
    runs_full/eliminated/bge.txt \
    runs_full/eliminated/e5.txt \
    runs_full/eliminated/bm25_e5_rerank.txt \
    runs_full/eliminated/hybrid_rrf_bm25_e5.txt \
  --k 10


## Condardance agreement on IR

python srs/concordance_ir.py \
  --qrels inputs/ir/qrels_kept_dpel.txt \
  --runs \
    runs_full/kept/bm25.txt \
    runs_full/kept/bge.txt \
    runs_full/kept/e5.txt \
    runs_full/kept/bm25_e5_rerank.txt \
    runs_full/kept/hybrid_rrf_bm25_e5.txt \
  --k 10 \
  --out-jsonl outputs/judging/analysis/concordance_kept_dpel.jsonl \
  --out-csv   outputs/judging/analysis/concordance_kept_dpel.csv

python srs/concordance_ir.py \
  --qrels inputs/ir/qrels_eliminated_dpel.txt \
  --runs \
    runs_full/eliminated/bm25.txt \
    runs_full/eliminated/bge.txt \
    runs_full/eliminated/e5.txt \
    runs_full/eliminated/bm25_e5_rerank.txt \
    runs_full/eliminated/hybrid_rrf_bm25_e5.txt \
  --k 10 \
  --out-jsonl outputs/judging/analysis/concordance_eliminated_dpel.jsonl \
  --out-csv   outputs/judging/analysis/concordance_eliminated_dpel.csv

python srs/concordance_ir.py \
  --qrels inputs/ir/qrels_kept_schema.txt \
  --runs \
    runs_full/kept/bm25.txt \
    runs_full/kept/bge.txt \
    runs_full/kept/e5.txt \
    runs_full/kept/bm25_e5_rerank.txt \
    runs_full/kept/hybrid_rrf_bm25_e5.txt \
  --k 10 \
  --out-jsonl outputs/judging/analysis/concordance_kept_schema.jsonl \
  --out-csv   outputs/judging/analysis/concordance_kept_schema.csv

python srs/concordance_ir.py \
  --qrels inputs/ir/qrels_eliminated_schema.txt \
  --runs \
    runs_full/eliminated/bm25.txt \
    runs_full/eliminated/bge.txt \
    runs_full/eliminated/e5.txt \
    runs_full/eliminated/bm25_e5_rerank.txt \
    runs_full/eliminated/hybrid_rrf_bm25_e5.txt \
  --k 10 \
  --out-jsonl outputs/judging/analysis/concordance_eliminated_schema.jsonl \
  --out-csv   outputs/judging/analysis/concordance_eliminated_schema.csv




python srs/build_final_regraxref_dataset.py
python srs/inspect_final_stats.py

python srs/sample_for_ADGM_spot_check.py

##############
conda activate regrag_xref
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
export PATH="$JAVA_HOME/bin:$PATH"
export JVM_PATH="$JAVA_HOME/lib/server/libjvm.dylib"


python srs/rag_step1_retrieve.py \
  --passages data/passages_full.jsonl \
  --test-json outputs/final_dataset/DPEL/test.jsonl \
  --retriever bm25 \
  --bm25-index indexes/bm25_full \
  --topk 50 \
  --out-jsonl outputs/rag/DPEL_test_bm25_retrieval.jsonl


python srs/rag_step1_retrieve.py \
  --passages data/passages_full.jsonl \
  --test-json outputs/final_dataset/DPEL/test.jsonl \
  --retriever e5 \
  --topk 50 \
  --out-jsonl outputs/rag/DPEL_test_e5_retrieval.jsonl


python srs/rag_step1_retrieve.py \
  --passages data/passages_full.jsonl \
  --test-json outputs/final_dataset/DPEL/test.jsonl \
  --retriever bge \
  --topk 50 \
  --out-jsonl outputs/rag/DPEL_test_bge_retrieval.jsonl


python srs/rag_step1_retrieve.py \
  --passages data/passages_full.jsonl \
  --test-json outputs/final_dataset/DPEL/test.jsonl \
  --retriever bm25_e5_rerank \
  --bm25-index indexes/bm25_full \
  --topk 50 \
  --out-jsonl outputs/rag/DPEL_test_bm25_e5_rerank_retrieval.jsonl


python srs/rag_step1_retrieve.py \
  --passages data/passages_full.jsonl \
  --test-json outputs/final_dataset/DPEL/test.jsonl \
  --retriever hybrid_rrf_bm25_e5 \
  --bm25-index indexes/bm25_full \
  --topk 50 \
  --out-jsonl outputs/rag/DPEL_test_hybrid_rrf_retrieval.jsonl


python srs/rag_step1_retrieve.py \
  --passages data/passages_full.jsonl \
  --test-json outputs/final_dataset/SCHEMA/test.jsonl \
  --retriever bm25 \
  --bm25-index indexes/bm25_full \
  --topk 50 \
  --out-jsonl outputs/rag/SCHEMA_test_bm25_retrieval.jsonl


python srs/rag_step1_retrieve.py \
  --passages data/passages_full.jsonl \
  --test-json outputs/final_dataset/SCHEMA/test.jsonl \
  --retriever e5 \
  --topk 50 \
  --out-jsonl outputs/rag/SCHEMA_test_e5_retrieval.jsonl


python srs/rag_step1_retrieve.py \
  --passages data/passages_full.jsonl \
  --test-json outputs/final_dataset/SCHEMA/test.jsonl \
  --retriever bge \
  --topk 50 \
  --out-jsonl outputs/rag/SCHEMA_test_bge_retrieval.jsonl


python srs/rag_step1_retrieve.py \
  --passages data/passages_full.jsonl \
  --test-json outputs/final_dataset/SCHEMA/test.jsonl \
  --retriever bm25_e5_rerank \
  --bm25-index indexes/bm25_full \
  --topk 50 \
  --out-jsonl outputs/rag/SCHEMA_test_bm25_e5_rerank_retrieval.jsonl


python srs/rag_step1_retrieve.py \
  --passages data/passages_full.jsonl \
  --test-json outputs/final_dataset/SCHEMA/test.jsonl \
  --retriever hybrid_rrf_bm25_e5 \
  --bm25-index indexes/bm25_full \
  --topk 50 \
  --out-jsonl outputs/rag/SCHEMA_test_hybrid_rrf_retrieval.jsonl


python srs/rag_step3_eval_retriever.py \
  --test-json outputs/final_dataset/DPEL/test.jsonl \
  --retrieval-json outputs/rag/DPEL_test_bm25_retrieval.jsonl \
  --k 10 \
  --out-json outputs/rag_eval/DPEL_test_bm25_k10_eval.json \
  --out-csv  outputs/rag_eval/DPEL_test_bm25_k10_eval.csv

python srs/rag_step3_eval_retriever.py \
  --test-json outputs/final_dataset/DPEL/test.jsonl \
  --retrieval-json outputs/rag/DPEL_test_e5_retrieval.jsonl \
  --k 10 \
  --out-json outputs/rag_eval/DPEL_test_e5_k10_eval.json \
  --out-csv  outputs/rag_eval/DPEL_test_e5_k10_eval.csv

python srs/rag_step3_eval_retriever.py \
  --test-json outputs/final_dataset/DPEL/test.jsonl \
  --retrieval-json outputs/rag/DPEL_test_bge_retrieval.jsonl \
  --k 10 \
  --out-json outputs/rag_eval/DPEL_test_bge_k10_eval.json \
  --out-csv  outputs/rag_eval/DPEL_test_bge_k10_eval.csv

python srs/rag_step3_eval_retriever.py \
  --test-json outputs/final_dataset/DPEL/test.jsonl \
  --retrieval-json outputs/rag/DPEL_test_bm25_e5_rerank_retrieval.jsonl \
  --k 10 \
  --out-json outputs/rag_eval/DPEL_test_bm25_e5_rerank_k10_eval.json \
  --out-csv  outputs/rag_eval/DPEL_test_bm25_e5_rerank_k10_eval.csv

python srs/rag_step3_eval_retriever.py \
  --test-json outputs/final_dataset/DPEL/test.jsonl \
  --retrieval-json outputs/rag/DPEL_test_hybrid_rrf_retrieval.jsonl \
  --k 10 \
  --out-json outputs/rag_eval/DPEL_test_hybrid_rrf_bm25_e5_k10_eval.json \
  --out-csv  outputs/rag_eval/DPEL_test_hybrid_rrf_bm25_e5_k10_eval.csv

python srs/rag_step3_eval_retriever.py \
  --test-json outputs/final_dataset/SCHEMA/test.jsonl \
  --retrieval-json outputs/rag/SCHEMA_test_bm25_retrieval.jsonl \
  --k 10 \
  --out-json outputs/rag_eval/SCHEMA_test_bm25_k10_eval.json \
  --out-csv  outputs/rag_eval/SCHEMA_test_bm25_k10_eval.csv

python srs/rag_step3_eval_retriever.py \
  --test-json outputs/final_dataset/SCHEMA/test.jsonl \
  --retrieval-json outputs/rag/SCHEMA_test_e5_retrieval.jsonl \
  --k 10 \
  --out-json outputs/rag_eval/SCHEMA_test_e5_k10_eval.json \
  --out-csv  outputs/rag_eval/SCHEMA_test_e5_k10_eval.csv

python srs/rag_step3_eval_retriever.py \
  --test-json outputs/final_dataset/SCHEMA/test.jsonl \
  --retrieval-json outputs/rag/SCHEMA_test_bge_retrieval.jsonl \
  --k 10 \
  --out-json outputs/rag_eval/SCHEMA_test_bge_k10_eval.json \
  --out-csv  outputs/rag_eval/SCHEMA_test_bge_k10_eval.csv

python srs/rag_step3_eval_retriever.py \
  --test-json outputs/final_dataset/SCHEMA/test.jsonl \
  --retrieval-json outputs/rag/SCHEMA_test_bm25_e5_rerank_retrieval.jsonl \
  --k 10 \
  --out-json outputs/rag_eval/SCHEMA_test_bm25_e5_rerank_k10_eval.json \
  --out-csv  outputs/rag_eval/SCHEMA_test_bm25_e5_rerank_k10_eval.csv

python srs/rag_step3_eval_retriever.py \
  --test-json outputs/final_dataset/SCHEMA/test.jsonl \
  --retrieval-json outputs/rag/SCHEMA_test_hybrid_rrf_retrieval.jsonl \
  --k 10 \
  --out-json outputs/rag_eval/SCHEMA_test_hybrid_rrf_bm25_e5_k10_eval.json \
  --out-csv  outputs/rag_eval/SCHEMA_test_hybrid_rrf_bm25_e5_k10_eval.csv

-----
python srs/rag_step2_generate_answers.py \
  --retrieval-json outputs/rag/DPEL_test_hybrid_rrf_retrieval.jsonl \
  --passages data/passages_full.jsonl \
  --model gpt-4o \
  --topk-contexts 10 \
  --out-jsonl outputs/rag_answers/DPEL_test_hybrid_rrf_gpt4o_k10.jsonl

python srs/rag_step2_generate_answers.py \
  --retrieval-json outputs/rag/SCHEMA_test_hybrid_rrf_retrieval.jsonl \
  --passages data/passages_full.jsonl \
  --model gpt-4o \
  --topk-contexts 10 \
  --out-jsonl outputs/rag_answers/SCHEMA_test_hybrid_rrf_gpt4o_k10.jsonl

python srs/rag_step2_generate_answers.py \
  --retrieval-json outputs/rag/DPEL_test_hybrid_rrf_retrieval.jsonl \
  --passages data/passages_full.jsonl \
  --model gpt-4o-mini \
  --topk-contexts 10 \
  --out-jsonl outputs/rag_answers/DPEL_test_hybrid_rrf_gpt4omini_k10.jsonl
python srs/rag_step2_generate_answers.py \
  --retrieval-json outputs/rag/SCHEMA_test_hybrid_rrf_retrieval.jsonl \
  --passages data/passages_full.jsonl \
  --model gpt-4o-mini \
  --topk-contexts 10 \
  --out-jsonl outputs/rag_answers/SCHEMA_test_hybrid_rrf_gpt4omini_k10.jsonl


python srs/rag_step4_eval_answers.py \
  --gold-json outputs/final_dataset/DPEL/test.jsonl \
  --pred-json outputs/rag_answers/DPEL_test_hybrid_rrf_gpt4o_k10.jsonl \
  --out-json outputs/rag_eval_answers/DPEL_test_hybrid_rrf_gpt4o_k10_eval_full.json \
  --out-csv  outputs/rag_eval_answers/DPEL_test_hybrid_rrf_gpt4o_k10_eval_full.csv \
  --nli-model-name MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli \
  --use-gpt-judge \
  --gpt-model gpt-4o-mini \
  --max-gpt-judge 0

python srs/rag_step4_eval_answers.py \
  --gold-json outputs/final_dataset/SCHEMA/test.jsonl \
  --pred-json outputs/rag_answers/SCHEMA_test_hybrid_rrf_gpt4o_k10.jsonl \
  --out-json outputs/rag_eval_answers/SCHEMA_test_hybrid_rrf_gpt4o_k10_eval_full.json \
  --out-csv  outputs/rag_eval_answers/SCHEMA_test_hybrid_rrf_gpt4o_k10_eval_full.csv \
  --nli-model-name MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli \
  --use-gpt-judge \
  --gpt-model gpt-4o-mini \
  --max-gpt-judge 0

python srs/rag_step4_eval_answers.py \
  --gold-json outputs/final_dataset/DPEL/test.jsonl \
  --pred-json outputs/rag_answers/DPEL_test_hybrid_rrf_gpt4omini_k10.jsonl \
  --out-json outputs/rag_eval_answers/DPEL_test_hybrid_rrf_gpt4omini_k10_eval_full.json \
  --out-csv  outputs/rag_eval_answers/DPEL_test_hybrid_rrf_gpt4omini_k10_eval_full.csv \
  --nli-model-name MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli \
  --use-gpt-judge \
  --gpt-model gpt-4o-mini \
  --max-gpt-judge 0

python srs/rag_step4_eval_answers.py \
  --gold-json outputs/final_dataset/SCHEMA/test.jsonl \
  --pred-json outputs/rag_answers/SCHEMA_test_hybrid_rrf_gpt4omini_k10.jsonl \
  --out-json outputs/rag_eval_answers/SCHEMA_test_hybrid_rrf_gpt4omini_k10_eval_full.json \
  --out-csv  outputs/rag_eval_answers/SCHEMA_test_hybrid_rrf_gpt4omini_k10_eval_full.csv \
  --nli-model-name MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli \
  --use-gpt-judge \
  --gpt-model gpt-4o-mini \
  --max-gpt-judge 0
---
---
# ============================
# DPEL – Gemini 2.5 Flash -lite
# ============================

python srs/rag_step2_generate_answers.py \
  --retrieval-json outputs/rag/DPEL_test_hybrid_rrf_retrieval.jsonl \
  --passages data/passages_full.jsonl \
  --model gemini-2.5-flash-lite \
  --topk-contexts 10 \
  --out-jsonl outputs/rag_answers/DPEL_test_hybrid_rrf_gemini25flashlite_k10.jsonl

python srs/rag_step2_generate_answers.py \
  --retrieval-json outputs/rag/SCHEMA_test_hybrid_rrf_retrieval.jsonl \
  --passages data/passages_full.jsonl \
  --model gemini-2.5-flash-lite \
  --topk-contexts 10 \
  --out-jsonl outputs/rag_answers/SCHEMA_test_hybrid_rrf_gemini25flashlite_k10.jsonl

python srs/rag_step4_eval_answers.py \
  --gold-json outputs/final_dataset/DPEL/test.jsonl \
  --pred-json outputs/rag_answers/DPEL_test_hybrid_rrf_gemini25flashlite_k10.jsonl \
  --out-json outputs/rag_eval_answers/DPEL_test_hybrid_rrf_gemini25flashlite_k10_eval_full.json \
  --out-csv  outputs/rag_eval_answers/DPEL_test_hybrid_rrf_gemini25flashlite_k10_eval_full.csv \
  --nli-model-name MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli \
  --use-gpt-judge \
  --gpt-model gpt-4o-mini \
  --max-gpt-judge 0

python srs/rag_step4_eval_answers.py \
  --gold-json outputs/final_dataset/SCHEMA/test.jsonl \
  --pred-json outputs/rag_answers/SCHEMA_test_hybrid_rrf_gemini25flashlite_k10.jsonl \
  --out-json outputs/rag_eval_answers/SCHEMA_test_hybrid_rrf_gemini25flashlite_k10_eval_full.json \
  --out-csv  outputs/rag_eval_answers/SCHEMA_test_hybrid_rrf_gemini25flashlite_k10_eval_full.csv \
  --nli-model-name MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli \
  --use-gpt-judge \
  --gpt-model gpt-4o-mini \
  --max-gpt-judge 0

