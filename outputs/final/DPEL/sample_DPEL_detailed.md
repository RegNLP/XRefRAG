# RegRAG-Xref sampled QAs

_Source file: `sample_DPEL_detailed.jsonl`_

## QA 1: DPEL — train

*persona: **professional** · reference_type: **Internal***

**QA ID:** `5efac2ed-0ae0-445c-b445-3ab200d0b984`

### Question

How should an Issuer treat Securities if the approval under Rule 9.7.5 lapses, and what conditions must be met for subsequent approval to be recognized under Rule 9.7.1?

### Expected answer

If the approval under Rule 9.7.5 lapses, the Securities can no longer be counted as Securities issued with approval under Rule 9.7.5 for the purposes of Rule 9.7.1. Instead, they are to be counted within Relevant Issues under Rule 9.7.1 [#SRC:76970fb8-577b-4a21-8996-4c8bde4ef2d2]. For subsequent approval to be recognized under Rule 9.7.1, the issue or agreement must not exceed the limit in Rule 9.7.1, the holders of the Listed Entity’s Ordinary Securities must subsequently approve it, and the Securities must be issued within three months of the date of the approval [#TGT:3f609871-988e-4e0c-921f-6e1066c630f6].

### Source passage

If the approval under Rule 9.7.5 lapses, the Securities can no longer be counted as Securities issued with approval under Rule 9.7.5 for the purposes of Rule 9.7.1 above, and instead are to be counted within Relevant Issues under Rule 9.7.1.

### Target passage

Subsequent approval of an issue of Securities. An issue of, or agreement to issue, Securities made without approval under Rule 9.7.1 is treated as having been made with approval for the purposes of Rule 9.7.1 if: (1) the issue or agreement did not exceed the limit in Rule 9.7.1; (2) the holders of the Listed Entity’s Ordinary Securities subsequently approve it; and (3) the Securities are issued within three months of the date of the approval.

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
- Methods with good answer: **5 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 2: DPEL — train

*persona: **professional** · reference_type: **Internal***

**QA ID:** `0169b104-dc53-4c00-b9fc-86a27e204ce3`

### Question

Under what circumstances may the Regulator take action against a Fund Manager or its Agent promoting a Passported Fund in ADGM, and what actions may be taken if the activities are materially prejudicial despite measures by the Home Regulator?

### Expected answer

The Regulator may take action against a Fund Manager, its Agent, or any other Licensed Person promoting a Passported Fund in ADGM if their activities continue to be materially prejudicial to the Unitholders situated in ADGM or to the financial stability or integrity of ADGM, despite any measures taken by the Home Regulator [#TGT:722d2090-eec8-4ae1-8d98-db9a10f13e55]. In such cases, the Regulator may prevent further promotion of the Passported Fund, de-register the fund from its Register of Passported Funds, or impose a penalty on the Fund Manager, its Agent, or any other Licensed Person, following consultation with the Home Regulator [#SRC:d4ba7643-bc71-443d-aab5-fac9738f8ae5].

### Source passage

Subject to Rule 9.5.2, the Regulator may take any action that is necessary and appropriate to enable it to further its objectives, including, but not limited to: (a) preventing the Fund Manager, its Agent or any other Licensed Person from further Promotion of the Passported Fund in ADGM, including de-registering the relevant Passported Fund from its Register of Passported Funds; and (b) imposing a penalty on the Fund Manager, its Agent or any other Licensed Person, of such amount as it considers appropriate under applicable ADGM legislation, following consultation with the Home Regulator.

### Target passage

If, despite the measures (if any) taken by a Home Regulator in relation to a Passported Fund, a Fund Manager's activities (or the activities of its Agent or any other Licensed Person that is Promoting the Passported Fund) in ADGM continue to be materially prejudicial to either: (a) the Unitholders of the Passported Fund who are situated in ADGM; or (b) the financial stability or the integrity of ADGM, the Regulator may request urgent discussions with the Home Regulator who has the supervision and enforcement responsibilities in respect of the Passported Fund.

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
- Methods with good answer: **4 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, BM25_E5_RERANK, E5, HYBRID_RRF
- Retrievers failing thresholds: BM25


---

## QA 3: DPEL — train

*persona: **professional** · reference_type: **External***

**QA ID:** `0f023c8a-c75c-4e19-bbbe-f739b7524de2`

### Question

Under what conditions does Behaviour constitute Market Abuse according to Section 92(6) of the FSMR, specifically in relation to the dissemination of information about Financial Instruments, Accepted Virtual Assets, or Accepted Spot Commodities?

### Expected answer

Behaviour constitutes Market Abuse under Section 92(6) of the FSMR when it involves disseminating information that gives, or is likely to give, a false or misleading impression regarding a Financial Instrument, an Accepted Virtual Asset, or an Accepted Spot Commodity. The person disseminating the information must have known, or could reasonably be expected to have known, that the information was false or misleading [#SRC:accbcc67-a2f7-4216-a57f-2e829b782418][#TGT:69005f53-8e03-4e6f-b2eb-82b1fff946ef].

### Source passage

Section 92(6) of the FSMR provides that Behaviour will amount to Market Abuse where it: "...consists of the dissemination of information by any means which gives, or is likely to give, a false or misleading impression as to a Financial Instrument, an Accepted Virtual Asset or an Accepted Spot Commodity by a person who knew or could reasonably be expected to have known that the information was false or misleading".

### Target passage

The fifth is where the Behaviour consists of the dissemination of information by any means which gives, or is likely to give, a false or misleading impression as to a Financial Instrument, an Accepted Virtual Asset or an Accepted Spot Commodity by a person who knew or could reasonably be expected to have known that the information was false or misleading.

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **10** (0–10)
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
- Methods with good answer: **4 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, BM25, E5, HYBRID_RRF
- Retrievers failing thresholds: BM25_E5_RERANK


---

## QA 4: DPEL — train

*persona: **professional** · reference_type: **External***

**QA ID:** `e94aa4e2-b42a-4d3f-aeb9-52e1e551fd4b`

### Question

Under what conditions can a person justify their conduct as legitimate when effecting transactions that might otherwise give a misleading impression or secure an artificial price level?

### Expected answer

A person can justify their conduct as legitimate if they can establish that their actions were carried out for legitimate reasons and in conformance with an Accepted Market Practice [#SRC:277b5e91-5efc-4b1d-a2b2-790aa0039f73]. This justification is necessary when the behaviour involves effecting transactions or orders to trade that might otherwise give a false or misleading impression regarding the supply, demand, or price of Financial Instruments, Accepted Virtual Assets, or Accepted Spot Commodities, or secure their price at an abnormal or artificial level [#TGT:e14e3ec9-c8a6-4747-a88e-b60c3395238f].

### Source passage

Market Practice. If a person establishes that they carried out the conduct or practice for legitimate reasons and in conformance with an Accepted Market Practice (see section 92(4)).

### Target passage

The third is where the Behaviour consists of effecting transactions or orders to trade (otherwise than for legitimate reasons and in conformity with Accepted Market Practices on the relevant market) which— (a) give, or are likely to give, a false or misleading impression as to the supply of, or demand for, or as to the price of, one or more Financial Instruments, Accepted Virtual Assets or Accepted Spot Commodities; or (b) secure the price of one or more such instruments at an abnormal or artificial level.

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **10** (0–10)
- Subscores: correctness=4, dual_use=4, realism=2

**IR retrieval concordance:**
- Number of relevant passages (qrels): **2**
- Evaluated at top-10 per retriever
- Methods hitting ≥1 relevant in top-10: **5** / 5
- Methods retrieving all relevant in top-10: **0** / 5
- High concordance (hit-any): **True**
- Low concordance (hit-any): **False**
- Retrievers with ≥1 relevant: bge.txt, bm25.txt, bm25_e5_rerank.txt, e5.txt, hybrid_rrf_bm25_e5.txt

**Answer quality / RAG concordance:**
- Methods with good answer: **4 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, BM25_E5_RERANK, E5, HYBRID_RRF
- Retrievers failing thresholds: BM25


---

## QA 5: DPEL — train

*persona: **basic** · reference_type: **Internal***

**QA ID:** `8a9ab27b-dc94-48d8-a73f-523ab6c22fda`

### Question

If the Regulator decides not to make a Recognition Order, what steps must it follow, and how does it handle written notices and representation opportunities?

### Expected answer

If the Regulator decides not to make a Recognition Order, it must follow specific steps, including providing a written notice to the Recognised Body or Applicant explaining the reasons for its decision and inviting them to make representations within a set timeframe [#SRC:5925da54-dd5e-4377-b2bb-22795223cb43]. The Regulator will consider any representations made and usually requires written representations before considering oral ones [#TGT:8f0e941a-957c-499b-952d-fa26d94c0efd]. If the Regulator chooses not to hear oral representations, it must inform the Recognised Body or Applicant promptly and allow more time for a response [#TGT:8f0e941a-957c-499b-952d-fa26d94c0efd]. After reaching a decision, the Regulator must notify the concerned party in writing [#TGT:8f0e941a-957c-499b-952d-fa26d94c0efd].

### Source passage

If the Regulator decides to refuse to make a Recognition Order, it will follow the procedure set out in Rule 6.9.6.

### Target passage

The procedures that the Regulator will follow in exercising its powers to make directions or refuse to make a Recognition Order (except in the case of a revocation of a Recognition Order, the Recognised Body concerned has given its consent or, in case where the Regulator proposes to make a direction, it considers it is reasonably necessary not to follow, or to cut short, the procedure) are: /Table Start The Regulator will: Guidance 1. give written notice to the Recognised Body (or Applicant); The notice will state why the Regulator intends to take the action it proposes to take, and include an invitation to make representations, and the period within which representations should be made (unless subsequently extended by the Regulator). 2. receive representations from the Recognised Body or Applicant concerned; The Regulator will not usually consider oral representations without first receiving written representations from the Recognised Body or Applicant. It will normally only hear oral representations from the Recognised Body or Applicant on request. 3. write promptly to the Recognised Body or Applicant who requests the opportunity to make oral representations if it decides not to hear that Person's representations; The Regulator will indicate why it will not hear oral representations and the Regulator will allow the Recognised Body or Applicant further time to respond. 4. have regard to representations made; 5. (when it has reached its decision) notify the Recognised Body or Applicant concerned in writing. /Table End

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **10** (0–10)
- Subscores: correctness=4, dual_use=4, realism=2

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
- Methods with good answer: **4 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BM25, BM25_E5_RERANK, E5, HYBRID_RRF
- Retrievers failing thresholds: BGE


---

## QA 6: DPEL — test

*persona: **professional** · reference_type: **External***

**QA ID:** `9787e3f8-593a-4eed-81f9-91b10cbca28e`

### Question

What are the obligations of an Authorised Person in relation to the Safe Custody Auditor's Report, and what specific details must the Auditor include in the report as per the requirements of the Regulator?

### Expected answer

An Authorised Person, whose Financial Service Permission allows them to hold Client Investments, is required to submit a Safe Custody Auditor's Report to the Regulator annually [#SRC:005cd89b-9c47-4377-a477-1b159acd9ba8]. In procuring this report, the Authorised Person must ensure that the Auditor includes specific details as of the date the Authorised Person's audited financial statement was prepared [#TGT:99e42871-85c3-4bd8-8cea-8366dc6a7607]. These details include the extent of the Authorised Person's activities in holding and controlling Client Investments, Arranging Custody, or Providing Custody [#TGT:99e42871-85c3-4bd8-8cea-8366dc6a7607]. Additionally, the Auditor must confirm whether the Authorised Person has maintained systems and controls to comply with the Safe Custody Rules in COBS Chapter 15 throughout the year, whether the Safe Custody Investments are properly registered, recorded, or held, and whether there have been any material discrepancies in the reconciliation of these investments [#TGT:99e42871-85c3-4bd8-8cea-8366dc6a7607]. The Auditor must also verify that they have received all necessary information and explanations for preparing the report and identify any unmet requirements of the Safe Custody Provisions [#TGT:99e42871-85c3-4bd8-8cea-8366dc6a7607].

### Source passage

In accordance with GEN 6.6.7, an Authorised Person whose Financial Service Permission entitles them to hold Client Investments must arrange for a Safe Custody Auditor's Report to be submitted to the Regulator on an annual basis.

### Target passage

Safe Custody Auditor's Report: An Authorised Person must, in procuring the production of a Safe Custody Auditor's Report by its Auditor, ensure that the Auditor states, as at the date on which the Authorised Person's audited statement of financial position was prepared: (1) the extent to which the Authorised Person was holding and controlling Client Investments, Arranging Custody or Providing Custody; and (2) whether: (a) the Authorised Person has, throughout the year, maintained systems and controls to enable it to comply with the Safe Custody Rules in COBS Chapter 15; (b) the Safe Custody Investments are registered, recorded or held in accordance with the Safe Custody Rules; (c) there have been any material discrepancies in the reconciliation of Safe Custody Investments; (d) the Auditor has received all necessary information and explanations for the purposes of preparing this report to the Regulator; and (e) any of the requirements of the Safe Custody Provisions have not been met.

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **10** (0–10)
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
- Methods with good answer: **5 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 7: DPEL — train

*persona: **professional** · reference_type: **External***

**QA ID:** `fa1f41d5-04ef-4d9f-88e4-060442ad935b`

### Question

Under what conditions may the Regulator approve the replacement of a Trustee, considering the independence requirements between a Trustee and a Fund Manager?

### Expected answer

The Regulator may approve the replacement of a Trustee if it receives a written notice from the Fund Manager indicating the intention to remove the Trustee, along with either a certification that the removal will not negatively impact the Unitholders or the Fund Manager's compliance capabilities, or a Special Resolution from the Unitholders approving the removal and replacement [#SRC:731c9d3a-6611-49d3-9ef9-2ddab7f4f1f2]. Additionally, the replacement Trustee must provide written consent and meet the requirements specified in Section 114(2) of the FSMR [#SRC:731c9d3a-6611-49d3-9ef9-2ddab7f4f1f2]. Furthermore, the Trustee must be independent of the Fund Manager, meaning there should be no shared voting rights, common holding companies, shared directors, shared individuals performing Controlled Functions, or recent professional dealings between the Fund Manager and the Trustee [#TGT:f90dee9e-41b0-46ee-b8ad-8ec88ec8b05c].

### Source passage

The Regulator may grant approval for the replacement of a Trustee only where it has received: (a) a written notice from the Fund Manager of its intention to remove the Trustee and either: (i) a certification that the removal of the Trustee will not adversely affect the interests of the Unitholders and the Fund Manager's ability to comply with its obligations under the Trust Deed, Prospectus, these Rules and the FSMR; or (ii) a Special Resolution of Unitholders approving the Fund Manager's proposal to remove the Trustee and its replacement with another Trustee; and (b) the written consent of the person who agrees to be the replacement Trustee, and that person meets the requirements for a Trustee in Section 114(2) of the FSMR to be able to act as the replacement Trustee.

### Target passage

The Trustee of an Investment Trust must be independent of the Fund Manager of that Investment Trust. A Trustee will not be independent of a Fund Manager if— (a) the Fund Manager or the Trustee holds, or exercise voting rights in respect of, any Shares of the other; (b) the Fund Manager and the Trustee have a common holding company or a common ultimate holding company; (c) the Fund Manager or the Trustee have Directors on its Governing Body, who are also Directors of the other; (d) the Fund Manager or the Trustee has individuals performing Controlled Functions who are also individuals performing Controlled Functions for the other; or (e) the Fund Manager and the Trustee have been involved in the previous two years in any professional or material business dealings, other than acting as Fund Manager or Trustee respectively of any other Fund.

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **10** (0–10)
- Subscores: correctness=4, dual_use=4, realism=2

**IR retrieval concordance:**
- Number of relevant passages (qrels): **2**
- Evaluated at top-10 per retriever
- Methods hitting ≥1 relevant in top-10: **5** / 5
- Methods retrieving all relevant in top-10: **4** / 5
- High concordance (hit-any): **True**
- Low concordance (hit-any): **False**
- Retrievers with ≥1 relevant: bge.txt, bm25.txt, bm25_e5_rerank.txt, e5.txt, hybrid_rrf_bm25_e5.txt
- Retrievers with all relevant: bge.txt, bm25.txt, bm25_e5_rerank.txt, hybrid_rrf_bm25_e5.txt

**Answer quality / RAG concordance:**
- Methods with good answer: **4 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, BM25_E5_RERANK, E5, HYBRID_RRF
- Retrievers failing thresholds: BM25


---

## QA 8: DPEL — train

*persona: **professional** · reference_type: **Internal***

**QA ID:** `8a08d781-a7b5-4754-9e73-f8aa6bd1a3c0`

### Question

What specific additional information must a Private Credit Fund include in its periodic reports, and how does this relate to the general requirements for Funds as outlined in Rule 16.4?

### Expected answer

A Private Credit Fund is required to include specific additional information in its periodic reports beyond the general requirements for Funds as outlined in Rule 16.4. This includes a detailed breakdown of originated loans by type, such as senior secured debt, junior debt, and mezzanine debt, as well as a summary of committed but undrawn Credit Facilities [#TGT:2c849a7d-71bb-4e57-acc5-fa50870faadf]. Additionally, the reports must provide a breakdown of loans by repayment schedule, the loan to value ratio for each loan, and information on non-performing exposures and forbearance activities [#TGT:2c849a7d-71bb-4e57-acc5-fa50870faadf]. Furthermore, the results of recent stress testing and any material changes to the credit assessment or monitoring process must be described [#TGT:2c849a7d-71bb-4e57-acc5-fa50870faadf]. This additional information complements the general information required by Rule 16.4, which is to be included in the periodic reports for Funds generally [#SRC:7199a7a2-6eb9-4183-b8c3-036c4c1dd5ed].

### Source passage

The information described in Rule 13A.6.1 should accompany the information to be included in the periodic reports required for Funds generally as set out in Rule 16.4.

### Target passage

In addition to the information required pursuant to these Rules, the periodic reports issued by a Private Credit Fund must include the following additional information: (h) a breakdown of the originated loans between senior secured debt, junior debt and mezzanine debt; (i) a summary of all committed but undrawn Credit Facilities; (j) a breakdown of the originated loans between loans made with an amortising repayment schedule and loans made with bullet repayments; (k) a breakdown of the loan to value ratio for each originated loan; (l) information in respect of non-performing exposures and exposures subject to forbearance activities; (m) a summary of the results of the most recent stress testing undertaken in accordance with Rules 13A.7.1 or 13A.7.2; and (n) a description of any material changes to the credit assessment or monitoring process of the Private Credit Fund.

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **10** (0–10)
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
- Methods with good answer: **5 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 9: DPEL — dev

*persona: **professional** · reference_type: **Internal***

**QA ID:** `a921969d-71f1-4a8f-88c6-bb35254bec7c`

### Question

How must an Authorised Person that is a Domestic Firm ensure compliance with liquidity and capital resource requirements to prevent significant risk of unmet liabilities?

### Expected answer

An Authorised Person that is a Domestic Firm must maintain both capital resources and liquid assets to ensure there is no significant risk that liabilities cannot be met as they fall due [#TGT:afbb9f59-2c26-47f6-ac38-4c36ecd40d56]. This involves holding sufficient immediately available cash or readily marketable assets, securing an appropriate matching future profile of cashflows, or further borrowing [#SRC:456ed7d2-778d-4597-862e-2c4582c20c87]. The capital resources must be of the types and amounts specified in the applicable rules, and they must be adequate in relation to the nature, size, and complexity of the business [#TGT:afbb9f59-2c26-47f6-ac38-4c36ecd40d56].

### Source passage

In accordance with Rule 3.2.2 or Rule 3.2.4, an Authorised Person is required to ensure that there is no significant risk that liabilities cannot be met as they fall due. With specific reference to liquidity, an Authorised Person may meet its obligations in a number of ways, including: a. by holding sufficient immediately available cash or readily marketable assets; b. by securing an appropriate matching future profile of cashflows; and c. by further borrowing.

### Target passage

Domestic Firms – maintaining capital resources. An Authorised Person that is a Domestic Firm must: (a) have and maintain, at all times, Capital Resources of the types and amounts specified in, and calculated in accordance with, these Rules; (b) ensure that it maintains capital and liquid assets in addition to the requirement in (a) which are adequate in relation to the nature, size and complexity of its business to ensure that there is no significant risk that liabilities cannot be met as they fall due.

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **9** (0–10)
- Subscores: correctness=4, dual_use=3, realism=2

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
- Methods with good answer: **4 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, BM25, BM25_E5_RERANK, E5
- Retrievers failing thresholds: HYBRID_RRF


---

## QA 10: DPEL — train

*persona: **professional** · reference_type: **Internal***

**QA ID:** `39e5d522-f118-4dca-adbb-b495f74f0108`

### Question

How must an MTF Operator or OTF Operator interpret references to Financial Instruments when complying with MIR rules, and what additional requirements must they adhere to under the MIR rulebook?

### Expected answer

An MTF Operator or OTF Operator must interpret references to Financial Instruments in the MIR rules as references to Virtual Assets, as applicable, when complying with the requirements set out in the MIR rulebook [#SRC:a3736367-db02-465d-809f-1bc6cfd7bbcd]. Additionally, these operators must adhere to specific requirements applicable to a Recognised Body or Recognised Investment Exchange, including operational systems and controls, transaction recording, membership criteria and access, financial crime and market abuse, rules and consultation, fair and orderly trading, pre-trade and post-trade transparency obligations, public disclosure, settlement and clearing services, default rules, and the use of Price Reporting Agencies [#TGT:180edda8-db12-4969-97d5-182435bdf094].

### Source passage

For the purposes of Rule 17.7.2, the following references in COBS, Chapter 8 should be read as follows: (a) references to Investment or Investments shall be read as references to Virtual Asset or Virtual Assets, as applicable; and (b) references to Financial Instrument or Financial Instruments (including those in MIR as incorporated by virtue of COBS Rule 8.2.1) shall be read as references to Virtual Asset or Virtual Assets, as applicable.

### Target passage

In addition to the general requirements applicable to Authorised Persons in COBS, GEN and elsewhere in the Rules, an Authorised Person carrying on the Regulated Activity of Operating an MTF (an "MTF Operator") or an Authorised Person carrying on the Regulated Activity of Operating an OTF (an “OTF Operator”) must comply with the following requirements applicable to a Recognised Body or Recognised Investment Exchange set out in the MIR rulebook, reading references to Recognised Bodies or Recognised Investment Exchanges in the relevant rules as if they were references to the MTF Operator or OTF Operator: (a) MIR 2.6 (Operational systems and controls); (b) MIR 2.7.1 and 2.7.2 (Transaction recording); (c) MIR 2.8 (Membership criteria and access); (d) MIR 2.9 (Financial crime and market abuse); (e) MIR 2.11 (Rules and consultation); (f) MIR 3.3 (Fair and orderly trading); (g) MIR 3.5 (Pre-trade transparency obligations); (h) MIR 3.6 (Post-trade transparency obligations); (i) MIR 3.7 (Public disclosure); (j) MIR 3.8 (Settlement and Clearing Services); (k) MIR 3.10 (Default Rules); and (l) MIR 3.11 (Use of Price Reporting Agencies).

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **10** (0–10)
- Subscores: correctness=4, dual_use=4, realism=2

**IR retrieval concordance:**
- Number of relevant passages (qrels): **2**
- Evaluated at top-10 per retriever
- Methods hitting ≥1 relevant in top-10: **5** / 5
- Methods retrieving all relevant in top-10: **0** / 5
- High concordance (hit-any): **True**
- Low concordance (hit-any): **False**
- Retrievers with ≥1 relevant: bge.txt, bm25.txt, bm25_e5_rerank.txt, e5.txt, hybrid_rrf_bm25_e5.txt

**Answer quality / RAG concordance:**
- Methods with good answer: **4 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, BM25, BM25_E5_RERANK, E5
- Retrievers failing thresholds: HYBRID_RRF


---

## QA 11: DPEL — train

*persona: **basic** · reference_type: **Internal***

**QA ID:** `197828ad-0d1c-4169-89f7-279c4bebc078`

### Question

When does a Domestic Firm need to have extra capital resources, and what is the Individual Capital Requirement (ICR)?

### Expected answer

A Domestic Firm needs to have extra capital resources when the Regulator imposes an Individual Capital Requirement (ICR) on it. This ICR requires the firm to hold additional Capital Resources from Pillar 2 adjustments, as specified in Rule 10.6.1, beyond the usual capital adequacy requirements in Rule 3.2.4 [#SRC:776c1fbb-de2a-4be6-b5fe-7b1666b6abff]. Additionally, the firm must ensure it has enough capital and liquid assets to match its business's nature, size, and complexity, so it can meet its liabilities on time [#TGT:afbb9f59-2c26-47f6-ac38-4c36ecd40d56].

### Source passage

Capital ratios. The Regulator may impose a further requirement, termed an Individual Capital Requirement (ICR), on an Authorised Person to hold additional Capital Resources arising from Pillar 2 adjustments (see Chapter 10). Where the Authorised Person has an ICR imposed on it, then the Authorised Person must, at all times, maintain adequate Capital Resources of the type and amount as specified in Rule 10.6.1 in addition to those kept to meet the capital adequacy requirements outlined in Rule 3.2.4.

### Target passage

Domestic Firms – maintaining capital resources. An Authorised Person that is a Domestic Firm must: (a) have and maintain, at all times, Capital Resources of the types and amounts specified in, and calculated in accordance with, these Rules; (b) ensure that it maintains capital and liquid assets in addition to the requirement in (a) which are adequate in relation to the nature, size and complexity of its business to ensure that there is no significant risk that liabilities cannot be met as they fall due.

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **9** (0–10)
- Subscores: correctness=4, dual_use=3, realism=2

**IR retrieval concordance:**
- Number of relevant passages (qrels): **2**
- Evaluated at top-10 per retriever
- Methods hitting ≥1 relevant in top-10: **5** / 5
- Methods retrieving all relevant in top-10: **4** / 5
- High concordance (hit-any): **True**
- Low concordance (hit-any): **False**
- Retrievers with ≥1 relevant: bge.txt, bm25.txt, bm25_e5_rerank.txt, e5.txt, hybrid_rrf_bm25_e5.txt
- Retrievers with all relevant: bge.txt, bm25.txt, bm25_e5_rerank.txt, hybrid_rrf_bm25_e5.txt

**Answer quality / RAG concordance:**
- Methods with good answer: **4 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, BM25, BM25_E5_RERANK, HYBRID_RRF
- Retrievers failing thresholds: E5


---

## QA 12: DPEL — dev

*persona: **professional** · reference_type: **Internal***

**QA ID:** `434e0299-92c6-4c4d-8452-500c22abb887`

### Question

Under what conditions may the parties agree to exclude the application of Rule 19.11.1(3) and Rule 19.20.1(4) concerning a Low Value Payment Instrument, and how does this relate to the Payer's liability for unauthorised Payment Transactions?

### Expected answer

The parties may agree to exclude the application of Rule 19.11.1(3) and Rule 19.20.1(4) when a Low Value Payment Instrument does not allow for the stopping or prevention of its use [#SRC:1db4fdad-1fa0-4aae-ad68-56d8705902d9]. This agreement is relevant to the Payer's liability for unauthorised Payment Transactions, as the Payer is generally not liable for losses incurred after notifying the Payment Service Provider of the loss, theft, or unauthorised use of the Payment Instrument, provided that the notification means were available as per Rule 19.11.1(3) [#TGT:bc276114-5360-4893-a879-9539f81273ce]. Therefore, if the parties agree to exclude these rules, the Payer may still be liable for certain losses unless other conditions, such as the Payment Service Provider's failure to apply Strong Customer Authentication, are met [#TGT:bc276114-5360-4893-a879-9539f81273ce].

### Source passage

The parties may agree that the following Rules do not apply where a Low Value Payment Instrument does not allow for the stopping or prevention of its use: (a) Rule 19.11.1 (3) (notification of loss of Payment Instrument); and (b) Rule 19.20.1(4) (Payer not liable for certain losses).

### Target passage

Subject to (1), except where the Payer has acted fraudulently, the Payer is not liable for any losses incurred in respect of an unauthorised Payment Transaction: (a) arising after notification to the Payment Service Provider in the agreed manner on becoming aware of the loss, theft, misappropriation or unauthorised use of the Payment Instrument; (b) where the Payment Service Provider has failed at any time to provide, in accordance with Rule 19.11.1(3), appropriate means for notification; (c) where the Payer’s Payment Service Provider has failed to apply Strong Customer Authentication; or (d) where the Payment Instrument has been used in connection with an Electronic Remote Payment Transaction.

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
- Methods with good answer: **5 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 13: DPEL — train

*persona: **professional** · reference_type: **Internal***

**QA ID:** `c84d0cf2-c3cf-4291-bdd6-49461d9c4cbf`

### Question

How should the Board of a Reporting Entity ensure compliance with Principle 7 regarding remuneration structures, and what specific reporting obligations must the Directors fulfill to demonstrate the business is a going concern?

### Expected answer

The Board of a Reporting Entity must ensure that remuneration structures and strategies are aligned with the long-term interests of the entity, as mandated by Principle 7 [#SRC:d6838b84-d2d6-4af0-b095-ee218f977826]. This requirement is similarly emphasized for a Listed Entity, indicating a consistent regulatory expectation across different entity types [#TGT:ee18ad4b-ba1c-41af-9b9d-96b923115a68]. Additionally, the Directors are obligated to report in both annual and half-yearly financial statements that the business is a going concern, providing any necessary supporting assumptions or qualifications [#SRC:d6838b84-d2d6-4af0-b095-ee218f977826]. This reporting obligation ensures transparency and accountability in financial disclosures, complementing the alignment of remuneration strategies with long-term interests [#TGT:ee18ad4b-ba1c-41af-9b9d-96b923115a68].

### Source passage

Other stakeholders. The Directors should report in annual and half yearly financial statements that the business is a going concern, with supporting assumptions or qualifications as necessary. Principle 7 Remuneration Rule 9.2.9 "The Board must ensure that the Reporting Entity has remuneration structures and strategies that are well aligned with the long term interests of the entity."

### Target passage

Principle 7 – Remuneration. The Board must ensure that the Listed Entity has remuneration structures and strategies that are well aligned with the long term interests of the Listed Entity.

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
- Methods with good answer: **4 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, BM25_E5_RERANK, E5, HYBRID_RRF
- Retrievers failing thresholds: BM25


---

## QA 14: DPEL — train

*persona: **professional** · reference_type: **Internal***

**QA ID:** `df6c6cec-03ac-4441-8aac-095c4e203ce2`

### Question

How should an Authorised Person calculate the pre-settlement Counterparty Exposure for an SFT when eligible financial Collateral is taken and a qualifying bilateral Netting agreement is in place?

### Expected answer

An Authorised Person must calculate the pre-settlement Counterparty Exposure for an SFT by recognising the effect of eligible financial Collateral in accordance with Rules 4.9.17 to 4.9.20 [#SRC:b2a0076b-8f51-4fc4-ac5b-6df2d25c4778]. If the SFT is covered by a qualifying bilateral Netting agreement and the Authorised Person is using the FCCA, they must calculate E* for all CR Exposures to any single Counterparty covered by the agreement, following Rules A4.3.2 to A4.3.6 in App4 [#TGT:56e2cb44-f613-4f2a-bd4c-8726a79a5776]. E* should then be substituted for E when determining the Credit Risk weighted Exposure amount for CR Exposures to that Counterparty under Section 4.8 [#TGT:56e2cb44-f613-4f2a-bd4c-8726a79a5776].

### Source passage

Measurement of E for pre settlement Counterparty Exposures arising from SFTs. An Authorised Person which has taken eligible financial Collateral for any SFT where the pre settlement Counterparty Exposure is determined in accordance with Rule 4.9.15 may recognise the effect of such Collateral in accordance with Rules 4.9.17 to 4.9.20.

### Target passage

Measurement of E for pre settlement Counterparty Exposures arising from SFTs. An Authorised Person which has taken eligible financial Collateral for an SFT that is covered by a qualifying bilateral Netting agreement and using the FCCA, must calculate E* for all its CR Exposures to any single Counterparty covered by the qualifying bilateral Netting agreement, in accordance with Rules A4.3.2 to A4.3.6 in App4 (if the Authorised Person is using supervisory haircuts or own estimate haircuts), and substitute E* for E when calculating the Credit Risk weighted Exposure amount for its CR Exposures to that Counterparty under Section 4.8.

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
- Methods with good answer: **5 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 15: DPEL — train

*persona: **basic** · reference_type: **External***

**QA ID:** `41c21486-4e4a-4a20-8d9a-17b2ae238892`

### Question

When can the Regulator tell someone that a law enforcement agency wants their interview answers, and what must happen for the Investigator to share those answers?

### Expected answer

The Regulator can inform someone if a law enforcement agency requests their interview answers for criminal proceedings, giving them a chance to agree to or contest the disclosure, unless a law or court order requires the Regulator to disclose it [#SRC:1e42ed63-f4af-4b44-9cb5-90fa843a8951]. For the Investigator to share those answers, the person must agree, or the Regulator must be legally required to disclose the information by law or court order [#TGT:c7705df9-fea6-4645-8706-3fe2fddac9ff].

### Source passage

If the Regulator receives a request from a law enforcement agency for a person's answers in an interview conducted under section 206(1)(a) of the FSMR for the purpose of criminal proceedings against the person, the Regulator will, in accordance with section 207(2) of the FSMR, generally notify the person concerned of such request (so that the person has an opportunity to either consent to the disclosure or challenge the request), unless the Regulator is required by law or court order to disclose the statement.

### Target passage

The Investigator shall not disclose a statement made by a person in answer to any question asked pursuant to a requirement made of the person under section ‎206‎(1)‎(a) to any law enforcement agency for the purpose of criminal proceedings against the person unless— (a) the person consents to the disclosure; or (b) the Regulator is required by law or court order to disclose the statement.

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **10** (0–10)
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
- Methods with good answer: **4 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, BM25, BM25_E5_RERANK, E5
- Retrievers failing thresholds: HYBRID_RRF


---

## QA 16: DPEL — train

*persona: **basic** · reference_type: **Internal***

**QA ID:** `1ac31e49-1be0-46ff-8d27-83cca750f8f0`

### Question

What happens to the Securities if approval under Rule 9.7.5 lapses, and how does this affect the number of new Equity Securities a company can issue without needing more approval?

### Expected answer

If approval under Rule 9.7.5 lapses, the Securities are no longer counted as approved under that rule and must be included in the Relevant Issues count [#SRC:76970fb8-577b-4a21-8996-4c8bde4ef2d2]. This affects how many new Equity Securities a company can issue without needing more approval because the Relevant Issues are subtracted from the maximum number calculated using the Base Amount [#TGT:a5d5f764-a746-4801-8e14-9584a84d3933]. As a result, the lapse of approval could reduce the number of new Equity Securities that can be issued without further approval [#TGT:a5d5f764-a746-4801-8e14-9584a84d3933].

### Source passage

If the approval under Rule 9.7.5 lapses, the Securities can no longer be counted as Securities issued with approval under Rule 9.7.5 for the purposes of Rule 9.7.1 above, and instead are to be counted within Relevant Issues under Rule 9.7.1.

### Target passage

Restrictions on new Issues of Equity Securities . A Listed Entity must not issue, or agree to issue, more Equity Securities than the number calculated according to the following formula, without the approval of the holders of Ordinary Securities: Maximum number of Equity Securities = (20% * Base Amount) – Relevant Issues), where: Base Amount = the number of fully paid Ordinary Securities on issue as of the date 12 months before the date of issue or agreement (the “12 months Base Amount”), plus the number of: (1) fully paid Ordinary Securities issued in the 12 months before the date of issue or agreement under an exception in Rule 9.7.4 other than exceptions (8), (15) or (16); (2) fully paid Ordinary Securities issued in the 12 months before the date of issue or agreement under an exception in Rule 9.7.4 other than exception (15), where the agreement was: (i) entered into before the commencement of the 12 month period; or (ii) approved, or taken under the Rules to have been approved, under Rule 9.7.1 or Rule 9.7.5; and (3) any other fully paid Ordinary Securities issued in the 12 months before the date of issue or agreement with approval under Rule 9.7.1 or Rule 9.7.5; Guidance The Base Amount may include fully paid Ordinary Securities issued in the 12 months before the date of issue or agreement under an agreement to issue Securities within Rule 9.7.4 exception (14) where the issue is subsequently approved under Rule 9.7.1. (4) partly paid Ordinary Securities that became fully paid in the 12 months before the date of issue or agreement, but subtracting the number of fully paid Ordinary Securities cancelled in the 12 months before the date of issue or agreement. Relevant Issues = the number of Equity Securities issued, or agreed to be issued, in the 12 months before the date of issue or agreement to issue other than: (a) with the approval of the holders of its Ordinary Securities under Rule 9.7.1 or Rule 9.7.5; or (b) under an exception in Rule 9.7.4.

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
- Methods with good answer: **4 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, BM25, E5, HYBRID_RRF
- Retrievers failing thresholds: BM25_E5_RERANK


---

## QA 17: DPEL — train

*persona: **basic** · reference_type: **Internal***

**QA ID:** `f13f3b12-c3a3-4810-ae0c-1632e7322ef0`

### Question

How must an Authorised Person manage a Spot Commodity Auction Platform to ensure it runs smoothly and keeps participants safe?

### Expected answer

An Authorised Person must have systems in place to operate a Spot Commodity Auction Platform effectively, including managing risks and monitoring participant transactions [#SRC:4056cfbb-4512-4279-a074-7577632f9653]. They must also ensure the platform runs in an orderly way and protects participants by having clear rules for auctions, transaction execution, and settlement processes [#TGT:1970af23-583d-4eee-8691-1db4637d6329]. Additionally, they are responsible for the technical operation of the platform and must have plans for any disruptions [#SRC:4056cfbb-4512-4279-a074-7577632f9653]. They should also take steps to prevent and detect Market Abuse or Financial Crime and provide necessary information to participants [#TGT:1970af23-583d-4eee-8691-1db4637d6329].

### Source passage

Systems and Controls. An Authorised Person must have adequate arrangements demonstrating that it: (a) can operate a Spot Commodity Auction Platform; (b) can assess, mitigate and manage the risks relating to the performance of a Spot Commodity Auction Platform; (c) monitors bids made by, and transactions effected by, participants on the Spot Commodity Auction Platform; (d) is responsible for, and performs, the full technical operation of the Spot Commodity Auction Platform, including in relation to contingency arrangements for disruption to the Spot Commodity Auction Platform; and (e) is responsible for, and operates, the arrangements set out in Rule 22.9.3.

### Target passage

Safeguards for Participants. An Authorised Person must ensure that business conducted on a Spot Commodity Auction Platform is conducted in an orderly manner and affords proper protection to participants, including: (a) by way of transparent rules and procedures: (i) to provide for fair and orderly auctions; (ii) to establish objective criteria for the efficient execution of transactions; and (iii) for the settlement of the Accepted Spot Commodity or transfer of the Spot Commodity Title; (b) in regards to the arrangements made for relevant information to be made available to participants on the Spot Commodity Auction Platform; (c) in regards to the arrangements made for recording transactions executed by participants on the Spot Commodity Auction Platform; (d) in regards to the measures adopted to reduce the extent to which the Spot Commodity Auction Platform’s facilities can be used for a purpose connected with Market Abuse or Financial Crime, and to facilitate their detection and monitor their influence; and (e) details of fees, costs and other charges, and the basis upon which the Authorised Person will impose those fees, costs and other charges.

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
- Methods with good answer: **5 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 18: DPEL — train

*persona: **basic** · reference_type: **Internal***

**QA ID:** `ec7a1b35-de80-42d4-a873-8747227b7e0e`

### Question

How do you figure out the Exposure value for Derivatives, like written credit protection, using both balance sheet rules and the SA-CCR method?

### Expected answer

To determine the Exposure value for Derivatives, including written credit protection, you need to add the on-balance sheet value calculated with IFRS to an add-on for potential future exposure, as outlined in Rules A4.6.14 to A4.6.21 of Appendix 4 [#SRC:b0cdb789-c9b6-4f36-a6b3-bf1e213d2007]. Additionally, using the Standardised Approach to Counterparty Credit Risk (SA-CCR), calculate the Exposure at Default (EAD) for each netting set with the formula EAD = alpha * (RC + PFE), where alpha is 1.4, RC is the replacement cost per Rules A4.6.19 to A4.6.24, and PFE is the potential future exposure per Rule A4.6.26 [#TGT:696b66b8-fa0b-4bd0-80cd-98ac02852918]. This ensures all aspects of exposure are covered.

### Source passage

In relation to on-balance sheet items: a. for SFTs, the Exposure value should be calculated in accordance with IFRS and the Netting requirements referred to in Rule 4.9.14; b. for Derivatives, including written credit protection, the Exposure value should be calculated as the sum of the on-balance sheet value in accordance with IFRS and an add-on for potential future Exposure calculated in accordance with Rules A4.6.14 to A4.6.21 of App 4; and c. for other on-balance sheet items, the Exposure value should be calculated based on their balance sheet values in accordance with Rule 4.9.3.

### Target passage

Derivatives and long settlement transactions – Standardised Approach to Counterparty Credit Risk (SA-CCR). EAD is to be calculated separately for each netting set. It is determined as follows: EAD = alpha* (RC + PFE) where: alpha = 1.4 RC = the replacement cost calculated according to Rules A4.6.19 to A4.6.24 PFE = the amount for potential future exposure calculated according to Rule A4.6.26

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
- Methods with good answer: **5 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 19: DPEL — train

*persona: **professional** · reference_type: **Internal***

**QA ID:** `5f49cd23-a24d-4acd-b89f-a959ee100a69`

### Question

What are the requirements for an Authorised Person regarding the deduction of capital instruments from AT1 and T2 Capital when significant investments in Relevant Entities are involved, and how do underwriting positions affect these deductions?

### Expected answer

An Authorised Person must deduct direct and indirect holdings of AT1 and T2 Capital instruments of Relevant Entities where it has a significant investment in those entities. However, underwriting positions held for five working days or fewer are excluded from these deductions for both AT1 and T2 Capital [#SRC:3bd61854-86d4-427f-9af0-54918b0e84c8][#TGT:5e7bdc23-7d1f-4fc2-8c33-dca7595021ab]. This exclusion allows temporary underwriting positions to be held without affecting the capital deductions, thereby providing flexibility in capital management while ensuring that long-term holdings are accurately reflected in the capital calculations.

### Source passage

AT1 Deductions. Subject to the following Rules in this Section, an Authorised Person must deduct the following from the calculation of its AT1 Capital: (a) direct and indirect holdings by an Authorised Person of own AT1 Capital instruments including instruments under which an Authorised Person is under an actual or contingent obligation to effect a purchase by virtue of an existing contractual obligation; (b) holdings of the AT1 Capital instruments of Relevant Entities where those entities have a reciprocal cross-holding with the Authorised Person which have the effect of artificially inflating the Capital Resources of the Authorised Person; (c) the amount determined in accordance with Rule 3.11.8 of direct and indirect holdings by the Authorised Person of the AT1 Capital instruments of Relevant Entities where the Authorised Person does not have a significant investment in those entities; (d) direct and indirect holdings by the Authorised Person of the AT1 Capital instruments of Relevant Entities where the Authorised Person has a significant investment in those entities, excluding Underwriting positions held for five working days or fewer; and (e) the amounts required to be deducted from T2 Capital pursuant to Rule 3.12.4 that exceed the T2 Capital of the Authorised Person.

### Target passage

T2 regulatory deductions and exclusions. Subject to the following Rules in this Section, an Authorised Person must deduct the following from the calculation of its T2 Capital: (a) direct and indirect holdings by an Authorised Person of own T2 Capital instruments, including own T2 instruments that an Authorised Person could be obliged to purchase as a result of existing contractual obligations; (b) holdings of the T2 Capital instruments of Relevant Entities where those entities have a reciprocal cross holding with the Authorised Person which have the effect of artificially inflating the Capital Resources of the Authorised Person; (c) the amount of direct and indirect holdings by the Authorised Person of the T2 Capital instruments of Relevant Entities where the Authorised Person does not have a significant investment in those entities; and (d) direct and indirect holdings by the Authorised Person of the T2 Capital instruments of Relevant Entities where the Authorised Person has a significant investment in those entities, excluding Underwriting positions held for fewer than five working days.

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **10** (0–10)
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
- Methods with good answer: **5 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 20: DPEL — train

*persona: **professional** · reference_type: **External***

**QA ID:** `a2496657-bd46-4994-b68c-89edb0c2589d`

### Question

What are the compliance obligations for an Authorised Person operating a Multilateral Trading Facility (MTF) when proposing to admit a new Accepted Virtual Asset to trading, considering the need to satisfy FSRA requirements and MIR Chapter 5 rules?

### Expected answer

An Authorised Person operating a Multilateral Trading Facility (MTF) must adhere to specific compliance obligations when proposing to admit a new Accepted Virtual Asset to trading. Firstly, the MTF must notify the FSRA of any new Accepted Virtual Asset it intends to admit to trading on its facilities, as required by COBS Rule 17.7.4 [#SRC:ac4da47e-f5d2-4ad6-8762-ac18e3eaf07a]. Additionally, the MTF must comply with the requirements set out in MIR, Chapter 5, which includes Rules 5.1 to 5.3 and Rule 5.4.1 under certain circumstances [#TGT:7404ef72-3a2f-4c07-a166-0dfd8a480e8d]. If the MTF's controls, such as those for identity or transaction monitoring, are not fully developed, the FSRA may require a delay in the commencement of trading until adequate controls are implemented [#SRC:ac4da47e-f5d2-4ad6-8762-ac18e3eaf07a].

### Source passage

REGULATORY REQUIREMENTS FOR AUTHORISED PERSONS ENGAGED IN REGULATED ACTIVITIES IN RELATION TO VIRTUAL ASSETS Accepted Virtual Assets An Accepted Virtual Asset may be deemed suitable for use by more than one Authorised Person, subject to each Authorised Person satisfying the FSRA that it can meet the regulatory requirements in respect of the specific Accepted Virtual Asset. For example, an MTF using Virtual Assets is required by COBS Rule 17.7.4 to notify the FSRA of any new Accepted Virtual Asset proposed to be admitted to trading on its facilities. Though the MTF may propose to admit to trading a commonly used and traded Virtual Asset, the MTFs controls, for example, relating to identity/transaction monitoring of a certain distributed ledger may not yet be fully developed. In such circumstances, the FSRA may require the MTF to delay the commencement of trading until such time that suitable controls have been developed and implemented.

### Target passage

An Authorised Person that is Operating a Multilateral Trading Facility in relation to Virtual Assets must comply with the following requirements set out in MIR, Chapter 5: (a) Rules 5.1 - 5.3; and (b) Rule 5.4.1, in the circumstances identified in Items 19, 20, 24 (a) and (b), 27, 28, 32, 33, 35, 37, 38, 39, 40, 41, 43, 45, 46, 47, 48, 49, 50, 52, 53, 54, 55, 57, 58, 59, 60, 61 and 62.

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **9** (0–10)
- Subscores: correctness=4, dual_use=4, realism=2

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
- Methods with good answer: **4 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, BM25_E5_RERANK, E5, HYBRID_RRF
- Retrievers failing thresholds: BM25


---

