# RegRAG-Xref sampled QAs

_Source file: `sample_DPEL_ir_failures.jsonl`_

## QA 1: DPEL — n/a

*persona: **basic** · reference_type: **External***

**QA ID:** `194cbaa9-4a01-4123-8001-97c31078fcce`

### Question

When Authorised Persons handle Virtual Assets, how should they understand 'Client Investments' in the rules, and why is this important?

### Expected answer

Authorised Persons should understand 'Client Investments' to include 'Virtual Assets' when handling them, as required by COBS Rule 17.8.2 [#SRC:15ac7d0d-8853-444c-8a24-8678075fa3c7]. This understanding is crucial because Rule 17.8.1 specifies that 'Investment' or 'Investments' should be read as including 'Virtual Asset' or 'Virtual Assets' [#TGT:1a0d0b8c-b8bf-48a1-b6ab-683d17ae56a0]. This ensures that Virtual Assets are protected similarly to other financial products under the FSMR and FSRA Rulebook [#SRC:15ac7d0d-8853-444c-8a24-8678075fa3c7].

### Source passage

AUTHORISED PERSONS PROVIDING CUSTODY OF VIRTUAL ASSETS In addition to having to meet the requirements set out in COBS Rules 17.1 to 17.6, Virtual Asset Custodians are required to meet the additional Rules set out in COBS Rule 17.8. COBS Rule 17.8.2 requires that the existing definitions of Client Assets and Client Investments be read to include Virtual Assets. This approach has been taken by the FSRA to ensure that Accepted Virtual Assets are afforded the same protections as other similar products and activities under FSMR and the FSRA Rulebook.

### Target passage

For the purposes of Rule 17.8.1 “Investment” or “Investments”, (and, a result, the corresponding references to “Client Investments”) shall be read as encompassing “Virtual Asset” or “Virtual Assets”, as applicable.

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **9** (0–10)
- Subscores: correctness=3, dual_use=4, realism=2

**IR retrieval concordance:**
- Number of relevant passages (qrels): **2**
- Evaluated at top-10 per retriever
- Methods hitting ≥1 relevant in top-10: **1** / 5
- Methods retrieving all relevant in top-10: **1** / 5
- High concordance (hit-any): **False**
- Low concordance (hit-any): **True**
- Retrievers with ≥1 relevant: hybrid_rrf_bm25_e5.txt
- Retrievers with all relevant: hybrid_rrf_bm25_e5.txt

**Answer quality / RAG concordance:**
- Methods with good answer: **0 / 5**
- High concordance on answer quality: **False**
- Low concordance on answer quality: **True**
- Retrievers failing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 2: DPEL — n/a

*persona: **basic** · reference_type: **Internal***

**QA ID:** `34a49344-e908-4cd3-85bd-c4d4d815a5f9`

### Question

How often must an Authorised Person check their Client Accounts, and what records do they need to keep?

### Expected answer

An Authorised Person must check their Client Accounts at least once every month to ensure accurate reconciliations [#TGT:2b1f7591-fc25-4d91-a3bd-88140fd07c1b]. They are required to keep records of these reconciliations in their Resolution Pack, as specified by Rules 14.11.1 and 15.9.1, which include the most recent reconciliations of Client Money and Client Investments [#SRC:803ff2b9-9528-459a-b9d2-45066785e9f5]. This process helps maintain transparency and accountability in their investment business operations.

### Source passage

The following records must be included in the Resolution Pack of an Authorised Person conducting Investment Business: (a) Rules 2.7.1 and 3.7.1(d) (records of Client classification and Client agreements); (b) Rules 14.6.2 and 15.4.3 (master lists of all Client Accounts in relation to Client Money and Client investments); (c) Rule 15.4.4 and Rule 15.4.5 (adequate records and Client's written permission re use of Client Investments); (d) Rules 14.7.1 and 14.7.4 (assessment of appropriateness of Third-Party Agent and acknowledgement by Third-Party agent in respect of Client Money); and (e) Rule 15.5.1 and 15.6.1 (assessment of appropriateness of Third Party Agent and acknowledgement by Third-Party Agent in respect of Client Investments); and (f) Rule 14.11.1 and 15.9.1 (most recent reconciliations of Client Money and Client Investments).

### Target passage

An Authorised Person conducting Investment Business must maintain adequate systems and controls to ensure that accurate reconciliations of Client Accounts are carried out as regularly as necessary but at least every calendar month.

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **9** (0–10)
- Subscores: correctness=3, dual_use=4, realism=2

**IR retrieval concordance:**
- Number of relevant passages (qrels): **2**
- Evaluated at top-10 per retriever
- Methods hitting ≥1 relevant in top-10: **0** / 5
- Methods retrieving all relevant in top-10: **0** / 5
- High concordance (hit-any): **False**
- Low concordance (hit-any): **True**

**Answer quality / RAG concordance:**
- Methods with good answer: **0 / 5**
- High concordance on answer quality: **False**
- Low concordance on answer quality: **True**
- Retrievers failing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 3: DPEL — n/a

*persona: **basic** · reference_type: **External***

**QA ID:** `a9f637d3-dab3-4131-a744-3cba0e3108e8`

### Question

If a Recognised Investment Exchange or Multilateral Trading Facility uses a Digital Settlement Facility instead of a Recognised Clearing House, what must they do, and how does this relate to a Recognised Clearing House's ability to settle transactions?

### Expected answer

A Recognised Investment Exchange (RIE) or Multilateral Trading Facility (MTF) must inform the Financial Services Regulatory Authority (FSRA) in writing about the satisfactory arrangements made when using a Digital Settlement Facility (DSF) instead of a Recognised Clearing House (RCH) [#SRC:cf09ad93-5f69-4c7f-8239-0281b7659c5e]. These arrangements must ensure that the DSF meets the requirements of MIR Rule 4.3.3, with references to a RCH being read as references to a DSF [#SRC:cf09ad93-5f69-4c7f-8239-0281b7659c5e]. Meanwhile, a Recognised Clearing House is not considered to have failed compliance just because it cannot settle a specific transaction [#TGT:a15123d3-b822-401d-9551-e8759dd9e84e]. This shows that while RIEs and MTFs have specific duties when using DSFs, RCHs have some leeway with transaction settlements.

### Source passage

DIGITAL SECURITIES SETTLEMENT Digital Settlement Facilities (DSFs) Pursuant to MIR Rule 3.8.3, however, and in the context of Digital Securities, a RIE or MTF must provide the FSRA, in writing, with the details of the satisfactory arrangements made when such RIE or MTF does not engage a RCH (for example, to use in this context, a DSF). To clarify, the FSRA will require that arrangements to use a DSF for settlement purposes will require the DSF to comply with the requirements of MIR Rule 4.3.3 (with the references to a RCH being read as references to a DSF).

### Target passage

A Recognised Clearing House will not be regarded as failing to comply with the Recognition Requirement merely because it is unable to arrange for a specific transaction to be settled.

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **9** (0–10)
- Subscores: correctness=4, dual_use=3, realism=2

**IR retrieval concordance:**
- Number of relevant passages (qrels): **2**
- Evaluated at top-10 per retriever
- Methods hitting ≥1 relevant in top-10: **0** / 5
- Methods retrieving all relevant in top-10: **0** / 5
- High concordance (hit-any): **False**
- Low concordance (hit-any): **True**

**Answer quality / RAG concordance:**
- Methods with good answer: **0 / 5**
- High concordance on answer quality: **False**
- Low concordance on answer quality: **True**
- Retrievers failing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 4: DPEL — n/a

*persona: **professional** · reference_type: **External***

**QA ID:** `54940f74-e9a4-4c78-b6ce-5a799e2e2531`

### Question

In the context of Digital Securities, what obligations must a Recognised Investment Exchange or Multilateral Trading Facility fulfill when opting to use a Digital Settlement Facility instead of a Recognised Clearing House, and how does this relate to the compliance expectations for a Recognised Clearing House regarding transaction settlement?

### Expected answer

A Recognised Investment Exchange (RIE) or Multilateral Trading Facility (MTF) must provide the Financial Services Regulatory Authority (FSRA) with written details of satisfactory arrangements when choosing to use a Digital Settlement Facility (DSF) instead of a Recognised Clearing House (RCH) for settlement purposes [#SRC:cf09ad93-5f69-4c7f-8239-0281b7659c5e]. These arrangements must ensure that the DSF complies with the requirements of MIR Rule 4.3.3, with references to a RCH being interpreted as references to a DSF [#SRC:cf09ad93-5f69-4c7f-8239-0281b7659c5e]. In parallel, a Recognised Clearing House will not be considered non-compliant with the Recognition Requirement merely because it is unable to arrange for a specific transaction to be settled [#TGT:a15123d3-b822-401d-9551-e8759dd9e84e]. This indicates that while RIEs and MTFs have specific obligations when using DSFs, RCHs have a degree of flexibility regarding individual transaction settlements.

### Source passage

DIGITAL SECURITIES SETTLEMENT Digital Settlement Facilities (DSFs) Pursuant to MIR Rule 3.8.3, however, and in the context of Digital Securities, a RIE or MTF must provide the FSRA, in writing, with the details of the satisfactory arrangements made when such RIE or MTF does not engage a RCH (for example, to use in this context, a DSF). To clarify, the FSRA will require that arrangements to use a DSF for settlement purposes will require the DSF to comply with the requirements of MIR Rule 4.3.3 (with the references to a RCH being read as references to a DSF).

### Target passage

A Recognised Clearing House will not be regarded as failing to comply with the Recognition Requirement merely because it is unable to arrange for a specific transaction to be settled.

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **9** (0–10)
- Subscores: correctness=3, dual_use=4, realism=2

**IR retrieval concordance:**
- Number of relevant passages (qrels): **2**
- Evaluated at top-10 per retriever
- Methods hitting ≥1 relevant in top-10: **1** / 5
- Methods retrieving all relevant in top-10: **0** / 5
- High concordance (hit-any): **False**
- Low concordance (hit-any): **True**
- Retrievers with ≥1 relevant: hybrid_rrf_bm25_e5.txt

**Answer quality / RAG concordance:**
- Methods with good answer: **0 / 5**
- High concordance on answer quality: **False**
- Low concordance on answer quality: **True**
- Retrievers failing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 5: DPEL — n/a

*persona: **basic** · reference_type: **Internal***

**QA ID:** `cd52cc4d-9859-4563-b85f-38f2a4ca50c8`

### Question

When can the Regulator tell a Recognised Body what to do about its Controllers, and what will they look at to decide if they should?

### Expected answer

The Regulator can tell a Recognised Body what to do about its Controllers if it thinks doing so will help achieve its goals [#TGT:1c3cd986-8007-416b-9fb1-e4600d1b1c81]. To decide if they should, the Regulator will look at all important information, including the MIR Rules, what they found during regular checks of the Recognised Body, and how not meeting the Recognition Requirements might affect their goals [#SRC:c6a75fa0-e9f4-459e-972a-a06f6236f8c6].

### Source passage

In considering whether it would be appropriate to exercise its powers to issue directions under Rule 6.6.1 or Rule 6.7.2, the Regulator will have regard to all relevant information and factors including: (a) the Rules contained in MIR; (b) the results of its routine supervision of the Recognised Body concerned; (c) the extent to which the failure or likely failure to satisfy one or more of the Recognition Requirements may affect the objectives of the Regulator.

### Target passage

The Regulator has the power to give a direction to a Recognised Body in matters relating to its Controllers if it considers that it is desirable to give the direction in order to advance one of more of its operational objectives.

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **9** (0–10)
- Subscores: correctness=4, dual_use=3, realism=2

**IR retrieval concordance:**
- Number of relevant passages (qrels): **2**
- Evaluated at top-10 per retriever
- Methods hitting ≥1 relevant in top-10: **0** / 5
- Methods retrieving all relevant in top-10: **0** / 5
- High concordance (hit-any): **False**
- Low concordance (hit-any): **True**

**Answer quality / RAG concordance:**
- Methods with good answer: **0 / 5**
- High concordance on answer quality: **False**
- Low concordance on answer quality: **True**
- Retrievers failing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 6: DPEL — n/a

*persona: **basic** · reference_type: **External***

**QA ID:** `e61bec81-e618-4ff3-a817-fa6624fb33ae`

### Question

When can the Regulator make a Reporting Entity share specific information or follow extra rules, and what must be true for this to happen?

### Expected answer

The Regulator can require a Reporting Entity to share specific information or follow extra rules if it believes doing so is in the best interest of the Abu Dhabi Global Market (ADGM) [#SRC:b83c251c-65fd-4f1c-9225-20fa42145c35]. The Regulator decides the terms and conditions for these actions [#TGT:5ed7d470-9d48-4676-936b-d27b5c945a94].

### Source passage

Section 84 of the FSMR gives the Regulator the power to direct a Reporting Entity to Disclose specified information or take such other steps as the Regulator considers appropriate where it is satisfied that it is in the interest of the ADGM to do so.

### Target passage

Miscellaneous . Regulator's powers of Direction The Regulator may, if it is satisfied that it is in the interests of the Abu Dhabi Global Market to do so— (a) direct a Reporting Entity to disclose specified information to the market or take such other steps as the Regulator considers appropriate; or (b) impose on a Reporting Entity any additional continuing obligations; on such terms and conditions as determined by the Regulator.

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **9** (0–10)
- Subscores: correctness=4, dual_use=4, realism=2

**IR retrieval concordance:**
- Number of relevant passages (qrels): **2**
- Evaluated at top-10 per retriever
- Methods hitting ≥1 relevant in top-10: **0** / 5
- Methods retrieving all relevant in top-10: **0** / 5
- High concordance (hit-any): **False**
- Low concordance (hit-any): **True**

**Answer quality / RAG concordance:**
- Methods with good answer: **0 / 5**
- High concordance on answer quality: **False**
- Low concordance on answer quality: **True**
- Retrievers failing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 7: DPEL — n/a

*persona: **basic** · reference_type: **External***

**QA ID:** `48089158-467f-44b6-9b1c-e0fe469b7a6d`

### Question

When can't an Insider share Inside Information, and how does this rule fit with the general rule about sharing such information?

### Expected answer

An Insider cannot share Inside Information with someone else unless it's part of their job, profession, or duties [#SRC:8f77978a-8215-43c3-a41b-20e6843ea3a6]. This rule fits with the general rule that also stops Insiders from sharing Inside Information outside their professional activities [#TGT:24c9495c-026d-446e-865a-9051fa94f13b].

### Source passage

Section 92(3) prohibits conduct where an Insider discloses Inside Information to another person otherwise than in the proper course of the exercise of his employment, profession or duties.

### Target passage

The second is where an Insider discloses Inside Information to another person otherwise than in the proper course of the exercise of his employment, profession or duties.

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **9** (0–10)
- Subscores: correctness=4, dual_use=4, realism=2

**IR retrieval concordance:**
- Number of relevant passages (qrels): **2**
- Evaluated at top-10 per retriever
- Methods hitting ≥1 relevant in top-10: **1** / 5
- Methods retrieving all relevant in top-10: **1** / 5
- High concordance (hit-any): **False**
- Low concordance (hit-any): **True**
- Retrievers with ≥1 relevant: e5.txt
- Retrievers with all relevant: e5.txt

**Answer quality / RAG concordance:**
- Methods with good answer: **0 / 5**
- High concordance on answer quality: **False**
- Low concordance on answer quality: **True**
- Retrievers failing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 8: DPEL — n/a

*persona: **basic** · reference_type: **External***

**QA ID:** `78871873-46ba-4c19-9c44-65008fc6845d`

### Question

When can the Regulator change the rules for admitting Securities to a Recognised Investment Exchange, and what else can it do about investments?

### Expected answer

The Regulator can change the rules for admitting Securities to a Recognised Investment Exchange if it thinks it's good for the ADGM [#SRC:1b705e19-5196-4730-b4a2-7a4d4e52ba8e]. It can also decide that something not usually considered a Security is a Security, or it can ignore certain requirements, as long as it sets terms it finds suitable [#TGT:95497208-1e94-4b51-8ff3-d9e77f64177c].

### Source passage

Waivers and modifications. The Regulator may, pursuant to section 58(2) of FSMR, waive or modify the application of the provisions in FSMR concerning the admission of Securities to trading on a Recognised Investment Exchange where it considers appropriate or desirable in the interests of the ADGM to do so and, in accordance with the procedures set out in paragraph 8 below.

### Target passage

Without limiting the generality of its powers, the Regulator may, by written notice— (a) exclude the application of any requirements; or (b) deem any investment which is not a Security to be a Security for the purposes of these Regulations and the Rules made under these Regulations; subject to such terms and conditions as it may consider appropriate.

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **9** (0–10)
- Subscores: correctness=4, dual_use=3, realism=2

**IR retrieval concordance:**
- Number of relevant passages (qrels): **2**
- Evaluated at top-10 per retriever
- Methods hitting ≥1 relevant in top-10: **1** / 5
- Methods retrieving all relevant in top-10: **0** / 5
- High concordance (hit-any): **False**
- Low concordance (hit-any): **True**
- Retrievers with ≥1 relevant: bge.txt

**Answer quality / RAG concordance:**
- Methods with good answer: **0 / 5**
- High concordance on answer quality: **False**
- Low concordance on answer quality: **True**
- Retrievers failing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 9: DPEL — n/a

*persona: **professional** · reference_type: **External***

**QA ID:** `f42725c7-278a-4a8d-8a6c-13425cf6a82e`

### Question

How must an Authorised Person ensure compliance with risk management requirements, considering both internal assessments and external reviews?

### Expected answer

An Authorised Person is required to establish and maintain risk management systems and controls that enable it to identify, assess, mitigate, control, and monitor its risks [#TGT:6f83c3c2-989d-47c2-952e-b1d8c7fb6c21]. Additionally, the firm must ensure these systems provide the means to manage risks effectively, as external reviews may assess the firm's internal risk self-assessment to determine the impact of risks on regulatory objectives and evaluate the likelihood of risks occurring [#SRC:f5c0b126-6b54-4fe9-9522-52952b6adad1].

### Source passage

Review of risk management systems. Under GEN 3.3.4, a firm must ensure that its risk management systems provide the firm with the means to identify, assess, mitigate, monitor and control its risks. In addition to undertaking our own assessment of the firm, we may review the firm's internal risk self-assessment and determine the extent to which each of the firm's risks impact our objectives, the likelihood of the risk occurring, and the controls and mitigation programmes the firm has in place.

### Target passage

Risk management: An Authorised Person must establish and maintain risk management systems and controls to enable it to identify, assess, mitigate, control and monitor its risks.

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **9** (0–10)
- Subscores: correctness=3, dual_use=4, realism=2

**IR retrieval concordance:**
- Number of relevant passages (qrels): **2**
- Evaluated at top-10 per retriever
- Methods hitting ≥1 relevant in top-10: **0** / 5
- Methods retrieving all relevant in top-10: **0** / 5
- High concordance (hit-any): **False**
- Low concordance (hit-any): **True**

**Answer quality / RAG concordance:**
- Methods with good answer: **0 / 5**
- High concordance on answer quality: **False**
- Low concordance on answer quality: **True**
- Retrievers failing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 10: DPEL — n/a

*persona: **basic** · reference_type: **Internal***

**QA ID:** `467b94ea-1daf-4d44-902b-6cba972ecd69`

### Question

When can a Recognised Investment Exchange delay sharing details about big trades, and what must it tell its Members and users?

### Expected answer

A Recognised Investment Exchange can delay sharing details about big trades if the trade is between a Member or Authorised Person and a Client, and the trade size is big enough according to Rule 3.6.10 [#TGT:d4233e73-f88e-4a70-8ab9-b5f982f14d48]. The delay must also fit within the time allowed for that type of Financial Instrument [#TGT:d4233e73-f88e-4a70-8ab9-b5f982f14d48]. The Exchange must inform its Members, users, and investors about the delay and its terms [#SRC:7f823646-b062-4581-a37a-a39040c4edad].

### Source passage

Deferrals. The Regulator may permit the requirements of Rule 3.6.1 to be deferred in respect of large volume or for certain types of trades, as specified in Rule 3.6.8, in which case the Recognised Investment Exchange must ensure that the existence of and the terms of the deferral are disclosed to Members and users of their facilities, and to investors.

### Target passage

Deferred publication of large transactions The deferred publication of information in respect of transactions may be authorised, for a period no longer than the period specified in Rule ‎3.6.10 for the class of Financial Instrument and transaction concerned, provided the following criteria are satisfied: (a) the transaction is between a Member or if applicable, Authorised Person, dealing on own account and a Client of that firm; and (b) the size of that transaction is equal to or exceeds the relevant minimum qualifying size, as specified in Rule 3.6.10. In order to determine the relevant minimum qualifying size, all Financial Instruments admitted to trading on a Recognised Investment Exchange shall be classified in accordance with their average daily turnover to be calculated in accordance with Rule 3.6.10.

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **9** (0–10)
- Subscores: correctness=4, dual_use=3, realism=2

**IR retrieval concordance:**
- Number of relevant passages (qrels): **2**
- Evaluated at top-10 per retriever
- Methods hitting ≥1 relevant in top-10: **1** / 5
- Methods retrieving all relevant in top-10: **0** / 5
- High concordance (hit-any): **False**
- Low concordance (hit-any): **True**
- Retrievers with ≥1 relevant: hybrid_rrf_bm25_e5.txt

**Answer quality / RAG concordance:**
- Methods with good answer: **0 / 5**
- High concordance on answer quality: **False**
- Low concordance on answer quality: **True**
- Retrievers failing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

