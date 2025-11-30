# RegRAG-Xref sampled QAs

_Source file: `sample_SCHEMA_ir_failures.jsonl`_

## QA 1: SCHEMA — n/a

*persona: **basic** · reference_type: **External***

**QA ID:** `202fe720-21a5-42aa-9c67-4be604e759e4`

### Question

What must an Authorised Person avoid when it comes to its total Exposure to a Counterparty or group of Closely Related Counterparties, especially concerning Large Exposures in the Non Trading and Trading Books?

### Expected answer

An Authorised Person must not let its total Exposure to a Counterparty or a group of Closely Related Counterparties go over 25% of its Capital Resources. This rule is part of the limits on Large Exposures. Specifically, the Authorised Person is prohibited from having any Large Exposures in its Non Trading Book that are more than 25% of its Tier 1 Capital. The same applies to its Trading Book, but with some conditions, like considering the impact of eligible Credit Risk Mitigation (CRM) measures. These rules help ensure that the Authorised Person manages its risk levels properly and stays within regulatory guidelines [#SRC:e27a19c6-b724-431d-8dd8-74cb76023956] and [#TGT:e70c0e97-fb04-4f48-9b0f-9aa5f025cd7f].

### Source passage

In accordance with PRU Rule 4.15.5, the aggregate of an Authorised Person's Exposure to a Counterparty or to a group of Closely Related Counterparties may not exceed 25% of the Authorised Person's Capital Resources.

### Target passage

Large Exposures limits. Subject to IFR Rule 5.4.15, an Authorised Person must not incur any Large Exposures in its Non Trading Book and, subject to Rule 4.15.6, Trading Book after taking into account the effect of any eligible CRM, that exceeds 25% of its Tier 1.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `aggregate of an Authorised Person's Exposure`
- Citation hook: `4.15.5`
- Source item type: `Prohibition`
- Target item type: `Prohibition`
- Answer spans: 1 span(s) annotated

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

## QA 2: SCHEMA — n/a

*persona: **professional** · reference_type: **External***

**QA ID:** `e18ad0e8-0c06-4b57-9da4-74b3081acf05`

### Question

What restrictions apply to an Authorised Person regarding the aggregate of its Exposure to a Counterparty or group of Closely Related Counterparties, particularly in relation to Large Exposures in both the Trading and Non Trading Books?

### Expected answer

An Authorised Person must ensure that the aggregate of its Exposure to a Counterparty or a group of Closely Related Counterparties does not exceed 25% of its Capital Resources. This restriction is crucial in maintaining compliance with Large Exposures limits. Specifically, the Authorised Person is prohibited from incurring any Large Exposures in its Non Trading Book that exceed 25% of its Tier 1 Capital, as well as in its Trading Book, subject to certain conditions. These conditions include taking into account the effect of any eligible Credit Risk Mitigation (CRM) measures. The prohibition ensures that the Authorised Person maintains a prudent level of risk exposure, thereby safeguarding its financial stability and adhering to regulatory requirements [#SRC:e27a19c6-b724-431d-8dd8-74cb76023956] and [#TGT:e70c0e97-fb04-4f48-9b0f-9aa5f025cd7f].

### Source passage

In accordance with PRU Rule 4.15.5, the aggregate of an Authorised Person's Exposure to a Counterparty or to a group of Closely Related Counterparties may not exceed 25% of the Authorised Person's Capital Resources.

### Target passage

Large Exposures limits. Subject to IFR Rule 5.4.15, an Authorised Person must not incur any Large Exposures in its Non Trading Book and, subject to Rule 4.15.6, Trading Book after taking into account the effect of any eligible CRM, that exceeds 25% of its Tier 1.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `aggregate of an Authorised Person's Exposure`
- Citation hook: `4.15.5`
- Source item type: `Prohibition`
- Target item type: `Prohibition`
- Answer spans: 1 span(s) annotated

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
- Methods with good answer: **1 / 5**
- High concordance on answer quality: **False**
- Low concordance on answer quality: **True**
- Retrievers passing thresholds: HYBRID_RRF
- Retrievers failing thresholds: BGE, BM25, BM25_E5_RERANK, E5


---

## QA 3: SCHEMA — n/a

*persona: **basic** · reference_type: **External***

**QA ID:** `1c9b8697-24c5-4186-9d1e-09268679663c`

### Question

What must a Mining Reporting Entity include in its disclosures about assumptions, and how does this connect to Ore Reserves rules?

### Expected answer

A Mining Reporting Entity must include all important economic assumptions in its disclosures when following certain rules. If any assumptions are sensitive, they need to explain why and how they determined them. These disclosures are crucial for creating financial forecasts and must also cover all other key assumptions and the Production Target. The rules for Ore Reserves, found in different codes like the JORC Code, SAMREC Code, and NI 43-101, add extra steps for classifying and sharing information about Ore Reserves. These codes help ensure that the information is detailed and follows industry standards. By connecting these disclosure needs with the Ore Reserves rules, stakeholders get a full and clear picture of the Mining Reporting Entity's financial predictions and resource assessments, as required [#TGT:4c6cbca4-a6c7-4b55-bebf-aeac86955d19] and permitted [#SRC:2c78a258-d9f2-4150-9d2c-ba681d8f9489].

### Source passage

A Mining Reporting Entitys disclosure pursuant to Rule 11.9.1 must include: (1) in relation to the assumptions used to determine the forecast financial information: (a) all material economic assumptions employed; (b) if the Mining Reporting Entity considers the material economic assumptions to be commercially sensitive, a statement to that effect and an explanation of the methodology used to determine the material economic assumptions; and Guidance A Mining Reporting Entity that considers certain information relating to the material economic assumptions to be commercially sensitive should refer to paragraphs 47-54 of the Guidance on Mining and paragraphs 127 and 128 of the Guidance on Continuous Disclosure. (c) all other material assumptions utilised. (2) the Production Target from which the forecast financial information is derived (including all the information contained in Rule 11.8.3).

### Target passage

ORE RESERVES . Clauses 29 to 36 of the JORC Code, Clauses 35 to 43 of the SAMREC Code and Part 2.2 (among others) of NI 43-101 set out additional requirements for the classification and disclosure of Ore Reserves.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `disclosure pursuant to ust include`
- Citation hook: `47-54`
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

## QA 4: SCHEMA — n/a

*persona: **basic** · reference_type: **Internal***

**QA ID:** `712fc029-d2f0-4039-88a1-b43b4c614a68`

### Question

What should the Fund Manager do when there are important changes, and what does the Regulator have to do after that?

### Expected answer

The Fund Manager of a Passported Fund must inform the Regulator as soon as possible about any important changes, following the rules set by ADGM. This should be done within seven days of knowing about the changes. After the Regulator gets this information, they must quickly tell the Host Regulator about these changes. This process helps make sure everyone who needs to know is kept up to date and follows the rules [#TGT:7a51b100-c0e6-41bd-809c-d2ae395a9898] and [#SRC:f1c064bd-93c8-459f-b7fa-fd9ed79b4669].

### Source passage

Upon receiving such a notification as described in Rule 6.6.2, the Regulator shall without undue delay notify the relevant Host Regulator of such changes.

### Target passage

The Fund Manager of a Passported Fund must notify the Regulator as soon as practicable of any material events, in accordance with applicable ADGM legislation. In particular (but without limitation), a Fund Manager or the governing body or trustee of a Passported Fund must notify the Regulator as soon as practicable (and in any case no later than seven days after it becomes aware) of any of the following events: (a) the Fund Manager intends to retire as manager of the Passported Fund; (b) it is proposed that a successor manager will be appointed in relation to the Passported Fund; (c) the Fund Manager has been removed or replaced as manager of the Passported Fund; (d) any material service provider to the Passported Fund (including, without limitation, any custodian) or an Agent or Licensed Person resigns, is appointed, is removed, or is replaced; (e) the Prospectus relating to the Passported Fund has been amended or replaced; (f) winding-up of the Passported Fund has commenced; or (g) the Fund Manager intends to vary or revoke its Financial Service Permission (or any conditions contained in that Financial Service Permission).

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `notify the relevant Host Regulator`
- Citation hook: `6.6.2`
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

## QA 5: SCHEMA — n/a

*persona: **basic** · reference_type: **External***

**QA ID:** `5da21302-a42a-4174-947e-d5a447c95c62`

### Question

When is an Insider not allowed to share Inside Information according to the rules?

### Expected answer

An Insider is not allowed to share Inside Information with someone else unless it is part of their job, profession, or duties. This rule is important to stop Market Abuse, which happens when someone uses Inside Information unfairly. Both the FSMR and related rules say that Insiders must keep Inside Information private unless sharing it is necessary for their work. This helps keep the market fair and prevents people from getting an unfair advantage. So, Insiders need to be careful and follow the rules to make sure they don't share Inside Information in the wrong way [#SRC:2099b5f8-78a0-43e7-8fc5-0295f590463e] and [#TGT:24c9495c-026d-446e-865a-9051fa94f13b].

### Source passage

Section 92(3) of the FSMR provides that Market Abuse will constitute instances where: "...an Insider discloses Inside Information to another person otherwise than in the proper course of the exercise of his employment, profession or duties."

### Target passage

The second is where an Insider discloses Inside Information to another person otherwise than in the proper course of the exercise of his employment, profession or duties.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `an Insider discloses Inside Information`
- Citation hook: `92(3)`
- Source item type: `Prohibition`
- Target item type: `Prohibition`
- Answer spans: 1 span(s) annotated

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
- Retrievers with ≥1 relevant: e5.txt

**Answer quality / RAG concordance:**
- Methods with good answer: **0 / 5**
- High concordance on answer quality: **False**
- Low concordance on answer quality: **True**
- Retrievers failing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 6: SCHEMA — n/a

*persona: **basic** · reference_type: **External***

**QA ID:** `9b2ea573-f0a5-43c3-9bf4-16e1c7f37fce`

### Question

When can the Regulator decide that an investment isn't a Security but should be treated as one, and what does the FSRA need from an Issuer to make this decision?

### Expected answer

The Regulator can decide to treat an investment that isn't normally a Security as a Security by issuing a written notice, as long as it finds the terms and conditions suitable. This decision is part of its broader powers under the regulations. For the FSRA to make this decision, an Issuer must provide enough information to show that their Digital Security fits the definition of a Security in the FSMR. This involves submitting specific documents, like an Approved Prospectus or Exempt Offer documentation, depending on the situation. The FSRA uses these documents to decide if the Digital Security can be considered a Security under the FSMR. This ensures that the Issuer meets all necessary regulatory requirements and that the Regulator's decision is based on complete and accurate information [#SRC:a8ffa89d-5c3e-41da-8f68-4b1795a0d986] [#TGT:95497208-1e94-4b51-8ff3-d9e77f64177c].

### Source passage

REGULATORY TREATMENT OF DIGITAL SECURITIES To use its powers under Section 58(2)(b), the FSRA expects that an Issuer will provide to it such information as is required to demonstrate that the proposed Digital Security meets the requirements of a Security (as defined in FSMR). In circumstances: a) requiring the submission of an Approved Prospectus to the FSRA, the FSRA will use the documentation submitted as part of this approval process to determine whether it will deem a Digital Security a Security under Section 58(2)(b) of FSMR; or b) relating to an Exempt Offer, the FSRA will review the Exempt Offer documentation for the purposes of being able to make a determination under Section 58(2)(b). The FSRAs review will not be for the purposes of approving the Exempt Offer itself.

### Target passage

Without limiting the generality of its powers, the Regulator may, by written notice— (a) exclude the application of any requirements; or (b) deem any investment which is not a Security to be a Security for the purposes of these Regulations and the Rules made under these Regulations; subject to such terms and conditions as it may consider appropriate.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `FSRA expects that an Issuer will provide`
- Citation hook: `58(2)(b)`
- Source item type: `Procedure`
- Target item type: `Permission`
- Answer spans: 1 span(s) annotated

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **9** (0–10)
- Subscores: correctness=4, dual_use=3, realism=2

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

## QA 7: SCHEMA — n/a

*persona: **professional** · reference_type: **External***

**QA ID:** `ae31e7e8-71c7-4035-aa8d-6d37f503ef9f`

### Question

Under what circumstances must an Issuer or Applicant not engage in conduct that contravenes the provisions set out by the Regulator, particularly when such conduct involves transactions or orders that might create a false or misleading market impression?

### Expected answer

An Issuer or Applicant must not engage in conduct that contravenes the provisions set out by the Regulator, specifically when such conduct involves effecting transactions or orders to trade that are not for legitimate reasons and do not conform with Accepted Market Practices. This is particularly relevant when these actions are likely to give a false or misleading impression regarding the supply, demand, or price of Financial Instruments, Accepted Virtual Assets, or Accepted Spot Commodities. Additionally, such conduct is prohibited if it aims to secure the price of these instruments at an abnormal or artificial level. The Regulator's views on these matters are crucial in determining the boundaries of acceptable conduct, ensuring that market integrity is maintained and that participants adhere to established standards [#SRC:20ea63b5-9f32-499a-8cb2-c2e120e41978] and [#TGT:e14e3ec9-c8a6-4747-a88e-b60c3395238f].

### Source passage

The following provisions of this Chapter set out the Regulator's views on conduct that contravenes paragraphs (a) and (b) of section 92(4).

### Target passage

The third is where the Behaviour consists of effecting transactions or orders to trade (otherwise than for legitimate reasons and in conformity with Accepted Market Practices on the relevant market) which— (a) give, or are likely to give, a false or misleading impression as to the supply of, or demand for, or as to the price of, one or more Financial Instruments, Accepted Virtual Assets or Accepted Spot Commodities; or (b) secure the price of one or more such instruments at an abnormal or artificial level.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `conduct that contravenes paragraphs`
- Citation hook: `92(4)`
- Source item type: `Scope`
- Target item type: `Prohibition`
- Answer spans: 1 span(s) annotated

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
- Retrievers with ≥1 relevant: hybrid_rrf_bm25_e5.txt
- Retrievers with all relevant: hybrid_rrf_bm25_e5.txt

**Answer quality / RAG concordance:**
- Methods with good answer: **2 / 5**
- High concordance on answer quality: **False**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, HYBRID_RRF
- Retrievers failing thresholds: BM25, BM25_E5_RERANK, E5


---

