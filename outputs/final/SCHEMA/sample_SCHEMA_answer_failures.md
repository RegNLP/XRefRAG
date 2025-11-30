# RegRAG-Xref sampled QAs

_Source file: `sample_SCHEMA_answer_failures.jsonl`_

## QA 1: SCHEMA — n/a

*persona: **basic** · reference_type: **External***

**QA ID:** `cd27d4d2-a2be-4413-a4c8-a333d4c1658e`

### Question

How often must an Authorised Person send statements to Retail Clients about their Accepted Virtual Assets, and how does this compare to the frequency for other Safe Custody Assets?

### Expected answer

An Authorised Person must send statements to Retail Clients about their Accepted Virtual Assets every month. This is more frequent than the requirement for other Safe Custody Assets, where statements must be sent at least every six months. This difference shows that virtual asset custodians have a stricter rule to follow, ensuring Retail Clients get more regular updates about their virtual asset holdings. This helps Retail Clients keep better track of their investments and ensures they are well-informed about their asset status. The regulatory rules are designed to make sure that Retail Clients receive timely and accurate information about their virtual assets, which is crucial for their financial decision-making [#SRC:0fb3a173-21f7-447a-9b86-6c07aede7c32] and [#TGT:c8d90cd9-2076-4aad-a6ae-6d57990ba0f8].

### Source passage

AUTHORISED PERSONS PROVIDING CUSTODY OF VIRTUAL ASSETS Safe Custody of Clients Virtual Assets Authorised Persons operating as Virtual Asset Custodians are required, with respect to the Accepted Virtual Assets they hold under custody for Clients, to: a) Send out statements of a Clients Accepted Virtual Assets holdings to Retail Clients at least monthly (as required under COBS Rule 15.8.1(a)); and b) Carry out all reconciliations of a Clients Accepted Virtual Asset holdings at least every week (as required under COBS Rule 15.9.1).

### Target passage

An Authorised Person which provides Custody or which otherwise holds or controls any Safe Custody Assets for a Client must send a regular statement to its Client: (a) if it is a Retail Client at least every six months; or (b) if it is a Professional Client at other intervals as agreed in writing with the Professional Client.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `send out statements of a Clients Accepted Virtual Assets`
- Citation hook: `15.8.1(a)`
- Source item type: `Obligation`
- Target item type: `Obligation`
- Answer spans: 1 span(s) annotated

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **9** (0–10)
- Subscores: correctness=4, dual_use=3, realism=2

**IR retrieval concordance:**
- Number of relevant passages (qrels): **2**
- Evaluated at top-10 per retriever
- Methods hitting ≥1 relevant in top-10: **5** / 5
- Methods retrieving all relevant in top-10: **5** / 5
- High concordance (hit-any): **True**
- Low concordance (hit-any): **False**
- Retrievers with ≥1 relevant: bge.txt, bm25.txt, bm25_e5_rerank.txt, e5.txt, hybrid_rrf_bm25_e5.txt
- Retrievers with all relevant: bge.txt, bm25.txt, bm25_e5_rerank.txt, e5.txt, hybrid_rrf_bm25_e5.txt

**Answer quality / RAG concordance:**
- Methods with good answer: **1 / 5**
- High concordance on answer quality: **False**
- Low concordance on answer quality: **True**
- Retrievers passing thresholds: BM25
- Retrievers failing thresholds: BGE, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 2: SCHEMA — n/a

*persona: **basic** · reference_type: **External***

**QA ID:** `f8968488-73e5-422d-891d-c26d91643a7f`

### Question

When does an Authorised Person not have to calculate its Foreign Exchange Risk Capital Requirement, considering its exposure to foreign currencies and gold and its Foreign Currency business size?

### Expected answer

An Authorised Person must calculate its Foreign Exchange Risk Capital Requirement if it is exposed to foreign currencies and gold under any Islamic Contract. However, it does not need to do this calculation if its Foreign Currency business, which is the greater of its total long or short positions in all Foreign Currencies, is not more than 100% of its Capital Resources. Also, it is exempt if its overall net open position is not more than 2% of its Capital Resources. These rules mean that only those with larger exposures need to calculate the requirement, making it easier for smaller businesses to comply [#SRC:6a51fe1f-d0d3-42f6-b369-4e9345775696] and [#TGT:79d3cd2f-93a5-4f25-af68-c67e7fd4cb97].

### Source passage

Market risk. An Authorised Person which is exposed to the risk of foreign currencies and gold under any Islamic Contract, must calculate its Foreign Exchange Risk Capital Requirement in accordance with PRU Rule 5.6.2.

### Target passage

An Authorised Person need not calculate a Foreign Exchange Risk Capital Requirement if: (a) its Foreign Currency business, defined as the greater of the sum of its gross long positions and the sum of its gross short positions in all Foreign Currencies, does not exceed 100% of Capital Resources as defined in Chapter 3; and (b) its overall net open position as defined in Rule A6.4.4 does not exceed 2% of its Capital Resources as defined in Chapter 3.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `calculate its Foreign Exchange Risk Capital Requirement`
- Citation hook: `5.6.2`
- Source item type: `Obligation`
- Target item type: `Prohibition`
- Answer spans: 1 span(s) annotated

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **9** (0–10)
- Subscores: correctness=4, dual_use=4, realism=2

**IR retrieval concordance:**
- Number of relevant passages (qrels): **2**
- Evaluated at top-10 per retriever
- Methods hitting ≥1 relevant in top-10: **5** / 5
- Methods retrieving all relevant in top-10: **5** / 5
- High concordance (hit-any): **True**
- Low concordance (hit-any): **False**
- Retrievers with ≥1 relevant: bge.txt, bm25.txt, bm25_e5_rerank.txt, e5.txt, hybrid_rrf_bm25_e5.txt
- Retrievers with all relevant: bge.txt, bm25.txt, bm25_e5_rerank.txt, e5.txt, hybrid_rrf_bm25_e5.txt

**Answer quality / RAG concordance:**
- Methods with good answer: **0 / 5**
- High concordance on answer quality: **False**
- Low concordance on answer quality: **True**
- Retrievers failing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 3: SCHEMA — n/a

*persona: **basic** · reference_type: **External***

**QA ID:** `88ea818a-9931-4a05-a488-aa5cbcfb85cc`

### Question

When do Recognised Investment Exchanges or Multilateral Trading Facilities need to tell the FSRA about using a Digital Settlement Facility, and what happens if a Recognised Clearing House can't settle a transaction?

### Expected answer

Recognised Investment Exchanges (RIEs) or Multilateral Trading Facilities (MTFs) need to inform the Financial Services Regulatory Authority (FSRA) in writing about their arrangements when they choose to use a Digital Settlement Facility (DSF) instead of a Recognised Clearing House (RCH). This is to ensure that the DSF meets certain regulatory standards. However, if a Recognised Clearing House cannot settle a specific transaction, it does not mean they are failing to meet their recognition requirements. This means that while RIEs and MTFs have to make sure their DSF arrangements are documented and compliant, a Recognised Clearing House is not considered non-compliant just because it can't settle a particular transaction. This provides some leeway for RCHs in specific situations, while keeping strict rules for RIEs and MTFs using DSFs [#SRC:cf09ad93-5f69-4c7f-8239-0281b7659c5e] and [#TGT:a15123d3-b822-401d-9551-e8759dd9e84e].

### Source passage

DIGITAL SECURITIES SETTLEMENT Digital Settlement Facilities (DSFs) Pursuant to MIR Rule 3.8.3, however, and in the context of Digital Securities, a RIE or MTF must provide the FSRA, in writing, with the details of the satisfactory arrangements made when such RIE or MTF does not engage a RCH (for example, to use in this context, a DSF). To clarify, the FSRA will require that arrangements to use a DSF for settlement purposes will require the DSF to comply with the requirements of MIR Rule 4.3.3 (with the references to a RCH being read as references to a DSF).

### Target passage

A Recognised Clearing House will not be regarded as failing to comply with the Recognition Requirement merely because it is unable to arrange for a specific transaction to be settled.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `arrangements to use a DSF for settlement`
- Citation hook: `4.3.3`
- Source item type: `Obligation`
- Target item type: `Scope`
- Answer spans: 1 span(s) annotated

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **9** (0–10)
- Subscores: correctness=4, dual_use=3, realism=2

**IR retrieval concordance:**
- Number of relevant passages (qrels): **2**
- Evaluated at top-10 per retriever
- Methods hitting ≥1 relevant in top-10: **4** / 5
- Methods retrieving all relevant in top-10: **0** / 5
- High concordance (hit-any): **True**
- Low concordance (hit-any): **False**
- Retrievers with ≥1 relevant: bge.txt, bm25_e5_rerank.txt, e5.txt, hybrid_rrf_bm25_e5.txt

**Answer quality / RAG concordance:**
- Methods with good answer: **0 / 5**
- High concordance on answer quality: **False**
- Low concordance on answer quality: **True**
- Retrievers failing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 4: SCHEMA — n/a

*persona: **basic** · reference_type: **Internal***

**QA ID:** `3c6911fc-a5a8-49c4-a370-a0d6c574f94d`

### Question

What must a Third Party Provider do to handle refunds for unauthorised transactions involving both the bank and the customer?

### Expected answer

A Third Party Provider must handle refunds for unauthorised transactions by addressing both the bank and the customer. If the bank has already refunded the customer, the provider must refund the bank for that amount. Additionally, the provider must refund the customer directly for the unauthorised transaction, but only after deducting any amount already refunded to the bank. This ensures that both parties are reimbursed correctly. The provider must act quickly, ensuring the customer receives their refund no later than the day after confirming the transaction was unauthorised or incorrect. This process ensures that all parties are treated fairly and promptly, maintaining trust in the transaction process [#SRC:74fba309-e803-4091-943a-510cb845f259] and [#TGT:5c21fe85-f19e-4984-bd0b-9f4b0d76bebe].

### Source passage

Third Party Providers liability for unauthorised Third Party Transactions. The Third Party Provider must provide a refund under Rule 20.12.1 as soon as practicable, and in any event no later than the end of the day following the day on which it has confirmed that the Third Party Transaction was unauthorised or incorrectly executed.

### Target passage

Third Party Provider’s liability for unauthorised Third Party Transactions. Subject to Rules 20.10 and 20.11, where an executed Third Party Transaction was not authorised in accordance with Rule 20.7 and the Third Party Transaction leads to an unauthorised Payment Transaction, the Third Party Provider must: (a) refund the Primary Financial Institution for the amount that the Primary Financial Institution may have already refunded to the Customer; and (b) refund the Customer for the amount of the unauthorised Payment Transaction, less any amount that the Third Party Provider has refunded to the Primary Financial Institution.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `must provide a refund`
- Citation hook: `20.12.1`
- Source item type: `Obligation`
- Target item type: `Obligation`
- Answer spans: 1 span(s) annotated

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **9** (0–10)
- Subscores: correctness=3, dual_use=4, realism=2

**IR retrieval concordance:**
- Number of relevant passages (qrels): **2**
- Evaluated at top-10 per retriever
- Methods hitting ≥1 relevant in top-10: **5** / 5
- Methods retrieving all relevant in top-10: **5** / 5
- High concordance (hit-any): **True**
- Low concordance (hit-any): **False**
- Retrievers with ≥1 relevant: bge.txt, bm25.txt, bm25_e5_rerank.txt, e5.txt, hybrid_rrf_bm25_e5.txt
- Retrievers with all relevant: bge.txt, bm25.txt, bm25_e5_rerank.txt, e5.txt, hybrid_rrf_bm25_e5.txt

**Answer quality / RAG concordance:**
- Methods with good answer: **0 / 5**
- High concordance on answer quality: **False**
- Low concordance on answer quality: **True**
- Retrievers failing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 5: SCHEMA — n/a

*persona: **basic** · reference_type: **Internal***

**QA ID:** `cf938a78-e7c3-43f5-a5ef-649660ab410e`

### Question

When a Mining Reporting Entity makes a statement about Exploration Targets, what must it do to fully meet all binding rules?

### Expected answer

A Mining Reporting Entity must make sure that any statement about Exploration Targets, Exploration Results, Mineral Resources, Ore Reserves, or Production Targets is prepared following a Mining Reporting Standard and the specific chapter that applies. This is important to fully meet all the binding rules. The Regulator requires that the entity not only follows the mandatory parts of the Mining Reporting Standard but also the non-mandatory parts, like those in the JORC Code or SAMREC Code, unless they explain why they didn't follow them. This ensures that all the information they provide is accurate and trustworthy, meeting both the technical and regulatory requirements [#SRC:b8235755-7447-4ae5-b3dc-8cb14109c124] and [#TGT:5d4c0697-2ff8-49a4-9682-8e63acb63b9d].

### Source passage

Rule 11.2.1(1) requires a Mining Reporting Entity to fully comply with all binding requirements set out in a Mining Reporting Standard. The Regulator also expects a Mining Reporting Entity to fully comply with all non-mandatory requirements set out in a Mining Reporting Standard, including, for example, Table 1 of the JORC Code or SAMREC Code, or explain its non-compliance in accordance with Rule 11.2.2.

### Target passage

Requirements for all disclosures. A disclosure by a Mining Reporting Entity that includes a statement about Exploration Targets, Exploration Results, Mineral Resources, Ore Reserves or Production Targets must be prepared in accordance with: (1) a Mining Reporting Standard; and (2) this chapter.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `fully comply with all binding requirements`
- Citation hook: `11.2.1(1)`
- Source item type: `Obligation`
- Target item type: `Obligation`
- Answer spans: 1 span(s) annotated

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **9** (0–10)
- Subscores: correctness=4, dual_use=4, realism=2

**IR retrieval concordance:**
- Number of relevant passages (qrels): **2**
- Evaluated at top-10 per retriever
- Methods hitting ≥1 relevant in top-10: **5** / 5
- Methods retrieving all relevant in top-10: **3** / 5
- High concordance (hit-any): **True**
- Low concordance (hit-any): **False**
- Retrievers with ≥1 relevant: bge.txt, bm25.txt, bm25_e5_rerank.txt, e5.txt, hybrid_rrf_bm25_e5.txt
- Retrievers with all relevant: bm25_e5_rerank.txt, e5.txt, hybrid_rrf_bm25_e5.txt

**Answer quality / RAG concordance:**
- Methods with good answer: **0 / 5**
- High concordance on answer quality: **False**
- Low concordance on answer quality: **True**
- Retrievers failing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 6: SCHEMA — n/a

*persona: **basic** · reference_type: **Internal***

**QA ID:** `86ef2570-b6a9-457c-ae99-534e2db05589`

### Question

What do Reporting Entities need to do to make sure they know about Inside Information and decide if it needs to be disclosed, given that their 'awareness' includes what Officers should reasonably know?

### Expected answer

Reporting Entities need to set up effective systems and procedures to ensure they are aware of Inside Information and can decide if it needs to be disclosed. This is important because their 'awareness' now includes not just what their Officers actually know, but also what they should reasonably know. This means that if anyone in the Listed Entity knows something significant, it should be brought to the Officers' attention. Without these systems, a Reporting Entity might delay or avoid its disclosure duties by claiming it didn't know about the Inside Information. Therefore, having the right internal processes and controls is crucial to make sure that any important Inside Information is quickly identified and assessed for disclosure. This helps the Reporting Entity meet its regulatory requirements and ensures timely decision-making [#SRC:515da637-1abc-4870-b98f-7ebda16f0984] and [#TGT:d437551a-aae1-4d57-94a7-fb36d8b2f879].

### Source passage

BECOMING AWARE OF INSIDE INFORMATION In regard to Rule 7.2.1, the first question that an Officer of a Reporting Entity should therefore consider is whether the Reporting Entity is aware of any Inside Information. If yes, that Officer must consider, immediately, whether that Inside Information must be Disclosed. Suitable systems and procedures must therefore be implemented by a Reporting Entity to ensure that Inside Information is promptly identified by, or within, a Listed Entity (in light of the awareness extension discussed in paragraph 38 above) and a decision is taken as to whether a Disclosure is required.

### Target passage

BECOMING AWARE OF INSIDE INFORMATION The extension of a Reporting Entity’s ‘awareness’ to include information that its Officers ‘ought reasonably have come into possession of’ (over and above information that its Officers, in fact, ‘know’) means that a Reporting Entity is considered to be ‘aware’ of Inside Information if the information is known by anyone within the Listed Entity, and is of such significance that it ought reasonably to have been brought to the attention of an Officer of the Listed Entity. Without this extension to the concept of ‘awareness’, a Reporting Entity would be able to avoid, or delay, meeting its continuous disclosure obligations in circumstances where Inside Information had not been brought to the attention of its Officers in a timely manner by others within the Listed Entity. A Listed Entity will need to ensure that it has in place internal systems, processes and controls to ensure that Inside Information is promptly brought to the attention of its Officers.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `systems and procedures must therefore be implemented`
- Citation hook: `38`
- Source item type: `Obligation`
- Target item type: `Definition`
- Answer spans: 1 span(s) annotated

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **9** (0–10)
- Subscores: correctness=3, dual_use=4, realism=2

**IR retrieval concordance:**
- Number of relevant passages (qrels): **2**
- Evaluated at top-10 per retriever
- Methods hitting ≥1 relevant in top-10: **5** / 5
- Methods retrieving all relevant in top-10: **4** / 5
- High concordance (hit-any): **True**
- Low concordance (hit-any): **False**
- Retrievers with ≥1 relevant: bge.txt, bm25.txt, bm25_e5_rerank.txt, e5.txt, hybrid_rrf_bm25_e5.txt
- Retrievers with all relevant: bge.txt, bm25_e5_rerank.txt, e5.txt, hybrid_rrf_bm25_e5.txt

**Answer quality / RAG concordance:**
- Methods with good answer: **0 / 5**
- High concordance on answer quality: **False**
- Low concordance on answer quality: **True**
- Retrievers failing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 7: SCHEMA — n/a

*persona: **basic** · reference_type: **Internal***

**QA ID:** `81b3bd0c-82c9-4bd6-83fd-d6b068e4bafe`

### Question

When can the Regulator allow changes to the rule about freely transferring Shares, and what must an Applicant do to get their Securities on the Official List?

### Expected answer

The Regulator can allow changes to the rule about freely transferring Shares if there are special circumstances. This can happen if the Applicant can stop the transfer of Shares without causing market problems. But to get their Securities on the Official List, the Applicant must follow certain rules: their Securities need to be properly authorised, have all needed consents, be freely transferable, and if they are Shares, they must be fully paid and without any liens or transfer restrictions. These steps ensure the Securities are valid and can be transferred as required [#TGT:bd978059-6701-4512-8a39-1f9364110d3a] and permitted [#SRC:7b5a94d4-4228-4d1a-b46a-d9f9dab0d14d].

### Source passage

The Regulator may, in exceptional circumstances, waive or modify Rule 2.3.8 where the Applicant has the power to disapprove the transfer of Shares, if the Regulator is satisfied that this power would not disturb the market in those Shares.

### Target passage

Validity and transferability. To be admitted to the Official List, an Applicant's Securities must: (1) be duly authorised according to the requirements of the Applicant's constitution; (2) have any necessary statutory or other consents; (3) be freely transferable; and (4) in the case of Shares, be fully paid and free from any liens and from any restrictions on the right of transfer.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `waive or modify`
- Citation hook: `2.3.8`
- Source item type: `Permission`
- Target item type: `Obligation`
- Answer spans: 1 span(s) annotated

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **9** (0–10)
- Subscores: correctness=4, dual_use=4, realism=2

**IR retrieval concordance:**
- Number of relevant passages (qrels): **2**
- Evaluated at top-10 per retriever
- Methods hitting ≥1 relevant in top-10: **5** / 5
- Methods retrieving all relevant in top-10: **1** / 5
- High concordance (hit-any): **True**
- Low concordance (hit-any): **False**
- Retrievers with ≥1 relevant: bge.txt, bm25.txt, bm25_e5_rerank.txt, e5.txt, hybrid_rrf_bm25_e5.txt
- Retrievers with all relevant: e5.txt

**Answer quality / RAG concordance:**
- Methods with good answer: **0 / 5**
- High concordance on answer quality: **False**
- Low concordance on answer quality: **True**
- Retrievers failing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 8: SCHEMA — n/a

*persona: **basic** · reference_type: **External***

**QA ID:** `7457e3ba-fd6b-433e-a775-6794650e5240`

### Question

What must an Authorised Person do to make sure their messages about Specified Investments or Regulated Activities are clear, fair, and not misleading?

### Expected answer

An Authorised Person must take reasonable steps to ensure that any communication they make to a Person about a Specified Investment or Regulated Activity is clear, fair, and not misleading. This means they need to check that the information they provide is easy to understand, honest, and does not give a wrong impression. This requirement is important because it helps people make informed decisions based on accurate information. It is part of the rules that keep financial markets fair and trustworthy. By following these steps, Authorised Persons help maintain the integrity of financial communications and protect investors from being misled. This obligation is in line with the broader regulatory standards that apply to financial communications, ensuring that all parties have access to reliable and truthful information [#SRC:48bcaa58-c3a9-4d7f-8042-bfb462cf2949] and [#TGT:a8ef44c9-fb33-4526-bbf5-6c7986418bb7].

### Source passage

COBS Rule 3.2.1 requires an Authorised Person to take reasonable steps to ensure that any communication to a Person in relation to a Specified Investment is clear, fair and not misleading. Similarly, chapter 4 of MKT sets out the requirements on a Person who makes or intends to make an Offer of Securities in ADGM. Without limiting any requirements under COBS or MKT, the Regulator has developed the ADGM Green Bond Designation and the ADGM Sustainability-Linked Bond Designation to indicate that an ADGM Issuer is issuing a debenture that it asserts is in accordance with Qualifying Green Debenture Principles or Qualifying Sustainability-Linked Debenture Principles.

### Target passage

When communicating information to a Person in relation to a Specified Investment or Regulated Activity, an Authorised Person must take reasonable steps to ensure that the communication is clear, fair and not misleading.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `take reasonable steps to ensure`
- Citation hook: `3.2.1`
- Source item type: `Obligation`
- Target item type: `Obligation`
- Answer spans: 1 span(s) annotated

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **9** (0–10)
- Subscores: correctness=4, dual_use=3, realism=2

**IR retrieval concordance:**
- Number of relevant passages (qrels): **2**
- Evaluated at top-10 per retriever
- Methods hitting ≥1 relevant in top-10: **5** / 5
- Methods retrieving all relevant in top-10: **2** / 5
- High concordance (hit-any): **True**
- Low concordance (hit-any): **False**
- Retrievers with ≥1 relevant: bge.txt, bm25.txt, bm25_e5_rerank.txt, e5.txt, hybrid_rrf_bm25_e5.txt
- Retrievers with all relevant: bm25.txt, hybrid_rrf_bm25_e5.txt

**Answer quality / RAG concordance:**
- Methods with good answer: **0 / 5**
- High concordance on answer quality: **False**
- Low concordance on answer quality: **True**
- Retrievers failing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 9: SCHEMA — n/a

*persona: **basic** · reference_type: **Internal***

**QA ID:** `4b71db12-1cb3-4b89-9412-6e8a8f943150`

### Question

How much insurance must a Third Party Provider have to cover both customer risks and transaction limits?

### Expected answer

A Third Party Provider must have enough professional indemnity insurance to cover any potential reimbursements to customers if something goes wrong due to operational risks. This means the provider needs to be prepared to pay back customers if needed. Additionally, the provider must ensure that the remaining insurance coverage is more than thirty times the average daily value of all transactions it handles over the last ninety days. This ensures that the provider has enough insurance to match the scale of its business activities. By meeting these requirements, the provider can protect itself and its customers from financial risks and stay compliant with regulations [#SRC:c9a29acd-37bb-40cb-9516-3121dbf18b53] and [#TGT:aaaa3ad8-9dea-490e-bd62-04177ed8aa0b].

### Source passage

Rule 6.12A.2 requires a Third Party Provider to maintain sufficient professional indemnity insurance coverage to reimburse Customers should operational risk events occur.

### Target passage

Transaction Limits. A Third Party Provider must ensure that its remaining professional indemnity insurance coverage is always greater than thirty times the average daily value of all Third Party Transactions in the past ninety calendar days.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `maintain sufficient professional indemnity insurance`
- Citation hook: `6.12A.2`
- Source item type: `Obligation`
- Target item type: `Obligation`
- Answer spans: 1 span(s) annotated

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **9** (0–10)
- Subscores: correctness=3, dual_use=4, realism=2

**IR retrieval concordance:**
- Number of relevant passages (qrels): **2**
- Evaluated at top-10 per retriever
- Methods hitting ≥1 relevant in top-10: **4** / 5
- Methods retrieving all relevant in top-10: **4** / 5
- High concordance (hit-any): **True**
- Low concordance (hit-any): **False**
- Retrievers with ≥1 relevant: bge.txt, bm25_e5_rerank.txt, e5.txt, hybrid_rrf_bm25_e5.txt
- Retrievers with all relevant: bge.txt, bm25_e5_rerank.txt, e5.txt, hybrid_rrf_bm25_e5.txt

**Answer quality / RAG concordance:**
- Methods with good answer: **0 / 5**
- High concordance on answer quality: **False**
- Low concordance on answer quality: **True**
- Retrievers failing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 10: SCHEMA — n/a

*persona: **basic** · reference_type: **Internal***

**QA ID:** `27d8be63-c942-4bd3-8300-f4ee669e68c8`

### Question

If a company wants to be both a Cell Company and a Captive Insurer, what fees do they need to pay to the Regulator?

### Expected answer

A company aiming to operate as both a Cell Company and a Captive Insurer must pay specific fees to the Regulator. For becoming a Cell Company, they need to pay an additional fee of $8,000, plus $1,000 for each Cell they plan to establish. At the same time, if they want to act as a Captive Insurer or an Insurance Special Purpose Vehicle, they must pay a separate fee of $5,000 for the Financial Services Permission to conduct insurance-related activities. These fees are necessary to comply with the regulatory requirements for operating in these roles [#SRC:eb333b78-8ff4-4f6f-bec8-65fa25c33fc0] and [#TGT:12672f4e-5d3b-4b17-b230-b8b95cfc9771].

### Source passage

Cell Companies. An Applicant under Rule 3.11.1 or Rule 3.11.3 that intends to operate as a Cell Company must pay to the Regulator an additional application fee of $8,000 for the Cell Company plus $1,000 for each Cell.

### Target passage

Captive Insurers and Insurance Special Purpose Vehicles. An Applicant for a Financial Services Permission must pay to the Regulator an application fee of $5,000 to carry on the Regulated Activity of Effecting Contracts of Insurance or Carrying Out Contracts of Insurance as: (a) a Captive Insurer; or (b) an Insurance Special Purpose Vehicle.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `must pay to the Regulator an additional application fee`
- Citation hook: `3.11.3`
- Source item type: `Obligation`
- Target item type: `Obligation`
- Answer spans: 1 span(s) annotated

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **9** (0–10)
- Subscores: correctness=4, dual_use=4, realism=2

**IR retrieval concordance:**
- Number of relevant passages (qrels): **2**
- Evaluated at top-10 per retriever
- Methods hitting ≥1 relevant in top-10: **5** / 5
- Methods retrieving all relevant in top-10: **1** / 5
- High concordance (hit-any): **True**
- Low concordance (hit-any): **False**
- Retrievers with ≥1 relevant: bge.txt, bm25.txt, bm25_e5_rerank.txt, e5.txt, hybrid_rrf_bm25_e5.txt
- Retrievers with all relevant: hybrid_rrf_bm25_e5.txt

**Answer quality / RAG concordance:**
- Methods with good answer: **0 / 5**
- High concordance on answer quality: **False**
- Low concordance on answer quality: **True**
- Retrievers failing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

