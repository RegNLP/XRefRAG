# RegRAG-Xref sampled QAs

_Source file: `sample_SCHEMA_detailed.jsonl`_

## QA 1: SCHEMA — train

*persona: **professional** · reference_type: **Internal***

**QA ID:** `09ea869a-aece-4090-8c48-8b2036e3fd7a`

### Question

What actions must an Authorised Person refrain from if it fails to meet the Combined Buffer Requirement, and what must it do before undertaking any distribution of profits?

### Expected answer

An Authorised Person that fails to meet the Combined Buffer Requirement is prohibited from undertaking certain actions until it has calculated the maximum distributable amount and notified the Regulator. Specifically, it must not make distributions related to CET1 Capital, create obligations for variable remuneration or discretionary pension benefits, or make payments on AT1 and T2 Capital instruments. Before proceeding with any distribution of profits, the Authorised Person must notify the Regulator and provide detailed information, including the amount of capital maintained, subdivided into CET1, AT1, and T2 Capital, as well as the amount of interim and year-end profits. Additionally, the maximum distributable amount must be calculated, and the intended allocation of distributable profits between dividend payments, share buybacks, payments on AT1 Capital instruments, and variable remuneration or discretionary pension benefits must be disclosed. This ensures compliance with regulatory requirements and prevents unauthorized distributions [#SRC:30965fe8-bf1e-44f4-9cd5-7e9b5f84a81e] [#TGT:e6d646b8-b830-4640-a03e-fabef741c603].

### Source passage

Restrictions on distributions. Where an Authorised Person fails to meet the Combined Buffer Requirement, it must: (a) calculate the maximum distributable amount in accordance with Rule 3.19.6; and (b) ensure that it does not undertake any of the following actions until such time as it has calculated the maximum distributable amount and notified the Regulator under Rule 3.19.7: (i) make a distribution in connection with CET1 Capital, or create an obligation to pay variable remuneration or discretionary pension benefits, or pay variable remuneration if the obligation to pay was created at a time when the institution failed to meet its Combined Buffer Requirement; or (ii) make payments on AT1 and T2 Capital instruments.

### Target passage

Restrictions on distributions. For the purpose of Rule 3.19.3(b), where an Authorised Person intends to distribute any of its distributable profits or intends to undertake an action referred to in Rule 3.19.3(b)(i) or (ii), the Authorised Person must notify the Regulator and provide the following information: (a) the amount of capital maintained by the Authorised Person, subdivided as follows: (i) CET1 Capital; (ii) AT1 Capital; and (iii) T2 Capital; (b) the amount of its interim and year-end profits; (c) the maximum distributable amount calculated in accordance with Rule 3.19.6; and (d) the amount of distributable profits it intends to allocate between the following: (i) dividend payments; (ii) Share buybacks; (iii) payments on AT1 Capital instruments; and (iv) the payment of variable remuneration or discretionary pension benefits, whether by creation of a new obligation to pay, or by payment pursuant to an obligation to pay created at a time when the institution failed to meet its Combined Buffer Requirement.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `it does not undertake any of the following actions`
- Citation hook: `3.19.7`
- Source item type: `Prohibition`
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
- Methods with good answer: **4 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, BM25_E5_RERANK, E5, HYBRID_RRF
- Retrievers failing thresholds: BM25


---

## QA 2: SCHEMA — dev

*persona: **professional** · reference_type: **Internal***

**QA ID:** `29c45055-19bb-46ee-a5ea-3817ea41fb84`

### Question

What are the requirements for a Reporting Listed Entity regarding the seniority and influence of the contact person who must be nominated to provide up-to-date contact details to the Regulator?

### Expected answer

A Reporting Listed Entity is required to ensure that the Regulator is provided with up-to-date contact details of persons nominated to act as the first point of contact concerning compliance with the Rules and the FSMR. The Regulator expects that the nominated contact person possesses sufficient seniority and influence, given the nature of the information they will handle and the critical role they play in maintaining compliance. This expectation underscores the importance of selecting individuals who can effectively communicate and manage compliance-related matters with the Regulator. Therefore, the entity must carefully choose a contact person who not only has the authority but also the capability to influence compliance processes and decisions within the organization. This dual requirement ensures that the contact person is both accessible and capable of addressing regulatory concerns effectively [#TGT:9c704216-6aa5-4988-807d-6f88f72d2b90] and [#SRC:907a9d98-54e0-4135-bfd0-6cb6b77c69a1].

### Source passage

The Regulator would expect a Reporting Entity's contact in Rule 2.8.6 to be of sufficient seniority and influence given the nature of the information which such Person would be dealing with and the importance of the role in maintaining the Listed Entity's compliance with the Rules and the FSMR.

### Target passage

Contact details. A Reporting Listed Entity must ensure that the Regulator is provided with up to date contact details of appropriate persons nominated by it to act as the first point of contact with the Regulator in relation to the Listed Entity's compliance with the Rules and the FSMR, as applicable.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `sufficient seniority and influence`
- Citation hook: `2.8.6`
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
- Methods with good answer: **5 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 3: SCHEMA — dev

*persona: **professional** · reference_type: **Internal***

**QA ID:** `536ab653-e141-431c-b467-b6c4bf3f9bc2`

### Question

Under what conditions may the Regulator require a Person to pay a supplementary fee when dealing with a request for a waiver or modification, and how does this relate to situations involving substantial additional costs or efforts?

### Expected answer

The Regulator is permitted to require a Person to pay a supplementary fee when dealing with a request for a waiver or modification if the request is deemed particularly complex or novel. This requirement aligns with the broader permission for the Regulator to impose such fees in circumstances where it anticipates incurring substantial additional costs or expending significant additional effort. These situations may arise during the processing of applications, authorisations, filings, or during ongoing supervision. The supplementary fee serves as a mechanism to ensure that the Regulator can adequately manage the resources needed to address these complex or resource-intensive situations effectively. By allowing for the imposition of supplementary fees, the Regulator ensures that it can maintain the necessary level of oversight and service without being unduly burdened by the additional demands of complex or novel requests [#SRC:ef45697b-2b10-450b-bacc-b9d501e87404] and [#TGT:64a0df5a-e946-4496-9fd3-244340c2a080].

### Source passage

In accordance with Rule 1.2.4, the Regulator may require a Person to pay a supplementary fee where the request for a waiver or modification is particularly complex or novel in the opinion of the Regulator.

### Target passage

Supplementary fees The Regulator may require a Person to pay to the Regulator a supplementary fee in circumstances where it expects to incur substantial additional costs or expend substantial additional effort in dealing with an application, authorisation, filing or when conducting on-going supervision.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `may require a Person to pay a supplementary fee`
- Citation hook: `1.2.4`
- Source item type: `Permission`
- Target item type: `Permission`
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
- Methods with good answer: **5 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 4: SCHEMA — train

*persona: **basic** · reference_type: **Internal***

**QA ID:** `30316681-bb99-463a-8a3a-bc657ab8f37e`

### Question

If a Recognised Investment Exchange uses a Clearing Service that isn't a Recognised Clearing House or a Non-Abu Dhabi Global Market Clearing House, what must they tell the Regulator in writing?

### Expected answer

When a Recognised Investment Exchange uses a Clearing Service that isn't a Recognised Clearing House or a Non-Abu Dhabi Global Market Clearing House, they must inform the Regulator in writing about the satisfactory arrangements they have made. These arrangements need to ensure that the rights and liabilities of the parties involved in transactions on the Recognised Investment Exchange are settled on time. This includes making sure that the clearing and settlement of these transactions are handled properly, whether through performance, compromise, or other methods. By confirming these arrangements in writing, the Recognised Investment Exchange demonstrates compliance with regulatory standards and ensures that the transaction processes are transparent and accountable. This requirement highlights the importance of both making the necessary arrangements and formally notifying the Regulator to maintain the integrity of the clearing and settlement processes [#SRC:58de7c59-691a-427d-b34d-d7fd9baf874e] and [#TGT:c56de460-9435-43a8-b170-bfe38c05a616].

### Source passage

If a Recognised Investment Exchange engages a party that is not a Recognised Clearing House or a Non-Abu Dhabi Global Market Clearing House, the Recognised Investment Exchange must confirm to the Regulator, in writing, the satisfactory arrangements made under Rule 3.8.1.

### Target passage

A Recognised Investment Exchange, when engaging a Clearing Service, must ensure that satisfactory arrangements are made for securing the timely discharge (whether by performance, compromise or otherwise), Clearing and settlement of the rights and liabilities of the parties to transactions effected on the Recognised Investment Exchange (being rights and liabilities in relation to those transactions).

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `confirm to the Regulator, in writing`
- Citation hook: `3.8.1`
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
- Methods retrieving all relevant in top-10: **0** / 5
- High concordance (hit-any): **True**
- Low concordance (hit-any): **False**
- Retrievers with ≥1 relevant: bge.txt, bm25.txt, bm25_e5_rerank.txt, e5.txt, hybrid_rrf_bm25_e5.txt

**Answer quality / RAG concordance:**
- Methods with good answer: **5 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 5: SCHEMA — train

*persona: **professional** · reference_type: **Internal***

**QA ID:** `02f9d484-6000-4df1-b9f1-7d9a1e9dccdd`

### Question

How must an Insurer account for the value of reinsurance and other recoveries expected to be received, and what is the requirement for treating premium liabilities related to future claim payments?

### Expected answer

An Insurer must treat as an asset the value of reinsurance and other recoveries expected to be received in respect of claims, ensuring compliance with International Financial Reporting Standards. Concurrently, the Insurer is obligated to treat as a liability the premium liability, which encompasses the value of future claim payments and associated direct and indirect settlement costs. These liabilities arise from future events insured under policies that are in force as of the Solvency Reference Date. This dual obligation ensures that the Insurer accurately reflects both the expected recoveries and the potential liabilities in its financial statements, maintaining a balanced and compliant financial position [#SRC:e6345a04-a9de-4dbf-8085-91eee4cffec6] and [#TGT:3c34e221-794b-4399-b4bd-b38a5f2a10c6].

### Source passage

An Insurer must treat as an asset the value of reinsurance and other recoveries expected to be received in respect of claims referred to in Rules 5.4.7 and 5.4.8 in accordance with International Financial Reporting Standards.

### Target passage

An Insurer must treat as a liability, the premium liability, which is the value of future claim payments and associated direct and indirect settlement costs, arising from future events insured under policies that are in force as at the Solvency Reference Date.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `treat as an asset the value of reinsurance`
- Citation hook: `5.4.7`
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
- Methods with good answer: **4 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, BM25_E5_RERANK, E5, HYBRID_RRF
- Retrievers failing thresholds: BM25


---

## QA 6: SCHEMA — train

*persona: **basic** · reference_type: **Internal***

**QA ID:** `aa0d1d1e-5358-4561-9e02-3f9f7ce75111`

### Question

Does an Authorised Person have to follow the Rules when preparing its returns, and can the Regulator change how often or in what way they submit them?

### Expected answer

An Authorised Person must prepare its returns according to the Rules, including guidelines and the Electronic Prudential Reporting System (EPRS) set by the Regulator. However, the Regulator can issue a written notice that allows the returns to be submitted in a different form, manner, or frequency than what is usually required. This change stays in place until the Regulator sends another written notice to adjust the submission process again. This setup ensures that while there is a standard way to prepare and submit returns, the Regulator can make changes if needed [#SRC:d384c02a-97aa-458d-9961-3b9b406ec6f9] and [#TGT:ceb0fc5a-9013-4a01-bf0c-a672333fcb3b].

### Source passage

An Authorised Person must, subject to Rule 2.3.3: (a) prepare its returns in accordance with the Rules in this Chapter, the instructional guidelines in PRU and elsewhere, and the requirements of the Electronic Prudential Reporting System (EPRS) of the Regulator including the frequency of submission detailed therein; and (b) submit the returns to the Regulator using EPRS.

### Target passage

The Regulator may by way of a written notice direct an Authorised Person to submit its returns in a form, manner or frequency other than as prescribed in Rule 2.3.2. An Authorised Person must continue to submit its returns in accordance with this direction until the Regulator by way of written notice directs otherwise.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `prepare its returns in accordance with the Rules`
- Citation hook: `2.3.3`
- Source item type: `Obligation`
- Target item type: `Permission`
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
- Methods with good answer: **4 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, BM25, BM25_E5_RERANK, HYBRID_RRF
- Retrievers failing thresholds: E5


---

## QA 7: SCHEMA — train

*persona: **basic** · reference_type: **Internal***

**QA ID:** `e2209d7a-520c-4600-9ddc-f7fdf11965cb`

### Question

If a Prospectus talks about Exploration Targets or similar things, what rules must it follow, and what must a Mining Reporting Entity do for its disclosures?

### Expected answer

A Prospectus that discusses Exploration Targets, Exploration Results, Mineral Resources, Ore Reserves, or Production Targets must follow certain rules, including Rule 11.2.1. It also needs to include details about how the Mining Reporting Entity handles environmental and social issues, the effects of its business on the environment and communities, and the risks it faces. At the same time, any disclosure by a Mining Reporting Entity that includes these topics must be prepared according to a Mining Reporting Standard and meet the chapter's requirements. This ensures that both the Prospectus and the disclosures are clear and meet the necessary standards for reporting mining activities [#SRC:ac70dcf0-7928-4d1c-9561-1b88ff273cb9] and [#TGT:5d4c0697-2ff8-49a4-9682-8e63acb63b9d].

### Source passage

In addition to complying with the requirements of Chapter 4, a Prospectus: (1) that includes a statement about Exploration Targets, Exploration Results, Mineral Resources, Ore Reserves or Production Targets, must comply with Rule 11.2.1; and (2) must include details in relation to the Mining Reporting Entitys policies and practices in relation to operating in a sustainable manner, including: (i) the Mining Reporting Entitys policy with regards to environmental and social issues; (ii) impact of the Mining Reporting Entitys business practices on the environment and the communities in which it operates; and (iii) the environmental and social risks faced by the Mining Reporting Entity.

### Target passage

Requirements for all disclosures. A disclosure by a Mining Reporting Entity that includes a statement about Exploration Targets, Exploration Results, Mineral Resources, Ore Reserves or Production Targets must be prepared in accordance with: (1) a Mining Reporting Standard; and (2) this chapter.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `must comply with`
- Citation hook: `11.2.1`
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
- Methods with good answer: **5 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 8: SCHEMA — train

*persona: **professional** · reference_type: **Internal***

**QA ID:** `e2cd356f-8333-4c1a-9caf-fcdece796c45`

### Question

What systems and procedures must a Reporting Entity implement to ensure compliance with the requirement to promptly identify and disclose Inside Information, considering the extension of 'awareness' to include information Officers ought reasonably to possess?

### Expected answer

A Reporting Entity must implement robust systems and procedures to ensure that Inside Information is promptly identified and assessed for disclosure obligations. This requirement arises from the extension of a Reporting Entity's 'awareness' to include not only information that its Officers actually know but also information that they ought reasonably to have come into possession of. This extension ensures that a Reporting Entity cannot avoid or delay its continuous disclosure obligations by claiming ignorance of Inside Information that should have been known. Therefore, the internal systems, processes, and controls must be designed to ensure that any significant Inside Information is promptly brought to the attention of the Officers within the Listed Entity. By doing so, the Reporting Entity can make timely decisions regarding the necessity of disclosure, thereby fulfilling its regulatory obligations effectively [#SRC:515da637-1abc-4870-b98f-7ebda16f0984] and [#TGT:d437551a-aae1-4d57-94a7-fb36d8b2f879].

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

## QA 9: SCHEMA — train

*persona: **basic** · reference_type: **Internal***

**QA ID:** `1c2a0388-b6a9-4e59-b27f-7f0a9a427791`

### Question

If Shareholders approve an agreement to issue Securities, what must happen within three months to keep the approval valid, and how does this connect to later approval steps?

### Expected answer

When Shareholders approve an agreement to issue Securities, the Issuer must issue those Securities within three months to keep the approval from lapsing. This is important because if the Securities were initially issued without approval, they can still be considered approved if they meet certain conditions. These conditions include not exceeding specific limits and getting subsequent approval from the holders of the Listed Entity’s Ordinary Securities. This subsequent approval also needs to happen within three months from the date of the initial approval. Therefore, the Issuer must manage the timing of both the issuance and any additional approvals to ensure everything stays valid and compliant [#SRC:6afde8f2-e0c2-4a55-afca-5f5b7d3cea35] and [#TGT:3f609871-988e-4e0c-921f-6e1066c630f6].

### Source passage

Subsequent approval of an issue of Securities. Where Shareholders approve an agreement to issue Securities under Rule 9.7.5, the Securities must be issued within three months of that approval or the approval will lapse.

### Target passage

Subsequent approval of an issue of Securities. An issue of, or agreement to issue, Securities made without approval under Rule 9.7.1 is treated as having been made with approval for the purposes of Rule 9.7.1 if: (1) the issue or agreement did not exceed the limit in Rule 9.7.1; (2) the holders of the Listed Entity’s Ordinary Securities subsequently approve it; and (3) the Securities are issued within three months of the date of the approval.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `Securities must be issued within three months`
- Citation hook: `9.7.5`
- Source item type: `Obligation`
- Target item type: `Procedure`
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
- Methods with good answer: **4 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BM25, BM25_E5_RERANK, E5, HYBRID_RRF
- Retrievers failing thresholds: BGE


---

## QA 10: SCHEMA — train

*persona: **professional** · reference_type: **External***

**QA ID:** `1fb95131-963d-42ee-8e9f-47f722235a97`

### Question

Under what circumstances must P not make a statement or conceal facts to avoid committing an offence or contravention, particularly when inducing actions related to Relevant Agreements or Designated Investments?

### Expected answer

P must not make a statement or conceal facts if doing so is intended to induce, or is reckless as to whether it may induce, another person to engage in specific financial activities. In the context of the FSMR, this includes entering into, offering to enter into, or refraining from entering or offering to enter into a Relevant Agreement, or exercising or refraining from exercising rights conferred by a Designated Investment. Similarly, under the Regulations, P commits a contravention if the statement or concealment is intended to induce, or is reckless as to whether it may induce, another person to enter into, offer to enter into, refrain from entering or offering to enter into, or to acquire, dispose of, subscribe for, underwrite, or refrain from acquiring, disposing of, subscribing for, or underwriting a Financial Instrument, Specified Investment, Accepted Virtual Asset, or Accepted Spot Commodity. Both contexts emphasize the prohibition against misleading actions that could influence another's financial decisions [#SRC:ccc1bc69-f5cb-4668-a23b-63b9c972177a] and [#TGT:bd2fec86-0605-4dc6-a24c-4e076626ca58].

### Source passage

Section 102(2) of the FSMR. Section 102(2) of the FSMR provides that a person ("P"): "...commits an offence if P makes the statement or conceals the facts with the intention of inducing, or is reckless as to whether making it or concealing them may induce, another person (whether or not the person to whom the statement is made)- (a) to enter into or Offer to enter into, or to refrain from entering or Offering to enter into, a Relevant Agreement, or (b) to exercise, or refrain from exercising, any rights conferred by a Designated Investment."

### Target passage

P commits a contravention of these Regulations if P makes the statement or conceals the facts with the intention of inducing, or is reckless as to whether making it or concealing them may induce, another person (whether or not the person to whom the statement is made) — (a) to enter into or offer to enter into, or to refrain from entering or offering to enter into; or (b) to acquire, dispose of, subscribe for or underwrite, or refrain from acquiring, disposing of, subscribing for or underwriting; or (c) to exercise, or refrain from exercising, any rights conferred by – a Financial Instrument, a Specified Investment, an Accepted Virtual Asset or an Accepted Spot Commodity, as applicable.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `commits an offence if P makes the statement`
- Citation hook: `102(2)`
- Source item type: `Prohibition`
- Target item type: `Prohibition`
- Answer spans: 1 span(s) annotated

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

## QA 11: SCHEMA — train

*persona: **professional** · reference_type: **Internal***

**QA ID:** `572eef91-7c7e-4808-8b6d-8270bff6ebb4`

### Question

Under what conditions must the Regulator permit and accompany an on-site inspection requested by a Host Regulator, and when may it refuse such cooperation?

### Expected answer

The Regulator is obligated to permit and accompany an on-site inspection requested by a Host Regulator concerning a Passported Fund, provided that certain conditions are met. However, the Regulator may refuse to cooperate if specific circumstances arise. These circumstances include situations where the Regulator has already initiated or concluded enforcement action regarding the same conduct and the same Persons, or if judicial proceedings have been initiated or concluded concerning the same conduct and the same Persons. This dual framework ensures that the Regulator fulfills its obligation to facilitate inspections while also retaining the discretion to refuse cooperation under defined conditions, thereby balancing regulatory cooperation with procedural integrity [#SRC:4b0be867-2636-45f5-aced-e11dd90b21c6] and [#TGT:cfff46fb-8811-4ce9-a5a9-a4f42576ca0c].

### Source passage

Where the Regulator receives a request from a Host Regulator to carry out an on-site inspection in relation to a Passported Fund, the Regulator shall, subject to Rule 9.3.2, permit such inspection and accompany it during the on-site inspection.

### Target passage

The Regulator may refuse to act on a request by a Host Regulator for cooperation in relation to an inspection in the following circumstances: (a) the Regulator has already commenced, or concluded, enforcement action in respect of the same conduct and the same Persons; or (b) judicial proceedings have already been initiated, or concluded, in respect of the same conduct and the same Persons.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `permit such inspection and accompany it`
- Citation hook: `9.3.2`
- Source item type: `Obligation`
- Target item type: `Permission`
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
- Methods with good answer: **4 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, BM25, BM25_E5_RERANK, HYBRID_RRF
- Retrievers failing thresholds: E5


---

## QA 12: SCHEMA — train

*persona: **professional** · reference_type: **Internal***

**QA ID:** `e411531a-39de-4c55-940d-ed458034e281`

### Question

What must a Mining Reporting Entity ensure when making a subsequent disclosure regarding Non-Equivalent Estimates that previously complied with the necessary requirements?

### Expected answer

A Mining Reporting Entity, when making a subsequent disclosure about Non-Equivalent Estimates that initially complied with the required standards, must ensure that the new disclosure references the earlier compliant disclosure. It must also confirm that the information from the initial disclosure remains applicable and that no new material information affects the reliability or interpretation of the estimates. Additionally, the subsequent disclosure must include a statement that is at least as prominent and proximate as the original, addressing the matters outlined in the initial requirements. This ensures that the subsequent disclosure maintains the integrity and transparency of the information provided, aligning with the obligation to disclose material Non-Equivalent Estimates of Mineralisation accurately. The entity must also ensure that the estimates are clearly identified as Non-Equivalent and not in accordance with a Mining Reporting Standard, and that a Competent Person has not classified them as Mineral Resources or Ore Reserves. This comprehensive approach ensures ongoing compliance and clarity in reporting [#SRC:21c96fff-8e3a-453f-9d85-4a922d8e7bf4] and [#TGT:df1ba511-2466-416a-9520-40451002811b].

### Source passage

If a Mining Reporting Entity has disclosed Non-Equivalent Estimates that comply with the requirements of Rule 11.7.3, then any subsequent disclosure made in respect of the Non-Equivalent Estimates does not need to include the information in that Rule if the subsequent disclosure: (1) references the earlier disclosure that was in compliance with that Rule; (2) contains a confirmation from the Mining Reporting Entity that: (a) the information provided in the earlier disclosure in compliance with that Rule continues to apply; and (b) there is no new material information or data relating to the Non-Equivalent Estimates that impacts on the: (i) reliability or interpretation of the Non-Equivalent Estimates; or (ii) Mining Reporting Entitys ability to verify the Non-Equivalent Estimates as Mineral Resources or Ore Reserves in accordance with a Mining Reporting Standard; and (3) includes an at least equally prominent, and proximate, statement about the disclosed Non-Equivalent Estimates addressing the matters contained in Rule 11.7.3(1).

### Target passage

A Mining Reporting Entity disclosing material Non-Equivalent Estimates of Mineralisation must ensure that the disclosure contains the following: (1) a prominent, and proximate, statement to the effect that: (a) the estimates are Non-Equivalent Estimates and are not disclosed in accordance with a Mining Reporting Standard; (b) a Competent Person has not done sufficient work to classify the Non-Equivalent Estimates as Mineral Resources or Ore Reserves in accordance with a Mining Reporting Standard; and (c) it is uncertain whether, following evaluation and/or further Exploration work, the Non-Equivalent Estimates will ever be able to be disclosed as Mineral Resources or Ore Reserves in accordance with a Mining Reporting Standard. (2) the source(s) and date(s) of the Non-Equivalent Estimates; (3) if the Non-Equivalent Estimates use categories of Mineralisation, a statement identifying whether the categories used: (a) are different to those defined in a Mining Reporting Standard, and an explanation of the differences; or (b) are the same as those defined in a Mining Reporting Standard; (4) the relevance of the Non-Equivalent Estimates to the Mining Reporting Entity; (5) the reliability of the Non-Equivalent Estimates; Guidance: For example, the Mining Reporting Entity may want to have regard to the relevant criteria listed in Table 1 of the JORC Code. (6) a summary of the evaluation and/or exploration work on which the Non-Equivalent Estimates are based; (7) a summary of the key assumptions, mining and processing parameters and methods used to prepare the Non-Equivalent Estimates; (8) details of any more recent estimates or data relevant to interpreting the Non-Equivalent Estimates, and the source(s) and date(s) of the estimates or data; (9) the evaluation and/or exploration work that needs to be undertaken to verify the Non-Equivalent Estimates as Mineral Resources or Ore Reserves in accordance with a Mining Reporting Standard; (10) the proposed timing of the evaluation and/or exploration work disclosed in (9); (11) the proposed source of funding for the evaluation and/or exploration work disclosed pursuant to (9); (12) the mineral resources classification and reporting standard used in determining the Non-Equivalent Estimates; and (13) a statement by a named Competent Person(s) that the information in the disclosure provided pursuant to (3) to (9) is an accurate representation of the available data and studies relating to the Non-Equivalent Estimates.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `subsequent disclosure made in respect of the Non-Equivalent Estimates`
- Citation hook: `11.7.3`
- Source item type: `Procedure`
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
- Methods with good answer: **4 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BM25, BM25_E5_RERANK, E5, HYBRID_RRF
- Retrievers failing thresholds: BGE


---

## QA 13: SCHEMA — dev

*persona: **basic** · reference_type: **Internal***

**QA ID:** `6c4effaf-4418-4ddd-9d04-37c35e835e55`

### Question

If a Mining Reporting Entity's disclosure doesn't follow a non-mandatory rule in a Mining Reporting Standard, what must it do to explain this?

### Expected answer

When a Mining Reporting Entity's disclosure does not meet a non-mandatory requirement in a Mining Reporting Standard, it must include a statement in its disclosure explaining how and why it differs from the requirement. This explanation is crucial for maintaining transparency and helps others understand the reasons behind the non-compliance. The entity must clearly outline both the nature of the non-compliance and the justification for it, ensuring that all stakeholders are informed about the deviations from the standard. This process is essential for upholding the integrity of the reporting system, as required [#TGT:211edfe0-af57-41c8-84ca-814e1af3de0f] and permitted [#SRC:b8235755-7447-4ae5-b3dc-8cb14109c124].

### Source passage

Rule 11.2.1(1) requires a Mining Reporting Entity to fully comply with all binding requirements set out in a Mining Reporting Standard. The Regulator also expects a Mining Reporting Entity to fully comply with all non-mandatory requirements set out in a Mining Reporting Standard, including, for example, Table 1 of the JORC Code or SAMREC Code, or explain its non-compliance in accordance with Rule 11.2.2.

### Target passage

Requirements for all disclosures. Where a disclosure by a Mining Reporting Entity does not meet a non-mandatory requirement contained in a Mining Reporting Standard, the Mining Reporting Entity must provide in its disclosure a statement as to how and why its disclosure differs from the non-mandatory requirement contained in the relevant Mining Reporting Standard.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `explain its non-compliance in accordance`
- Citation hook: `11.2.2`
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
- Methods with good answer: **4 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BM25, BM25_E5_RERANK, E5, HYBRID_RRF
- Retrievers failing thresholds: BGE


---

## QA 14: SCHEMA — train

*persona: **professional** · reference_type: **Internal***

**QA ID:** `b94ae994-b417-40b1-870b-d0ec8fde16af`

### Question

What must the Board of Directors of a Reporting Entity include in the annual report to ensure compliance with the Corporate Governance framework, and how should a Listed Entity address the adoption of best practice standards in its annual financial report?

### Expected answer

The Board of Directors of a Reporting Entity is required to include a statement in the annual report assessing whether the Corporate Governance framework is effective in achieving the desired outcomes and promoting compliance with the Principles. This statement must be supported by relevant information, assumptions, and any necessary qualifications. Concurrently, a Listed Entity must address the adoption of best practice standards in its annual financial report by stating whether these standards have been adopted. If not fully adopted, the report should explain the reasons for partial or non-adoption and outline any actions taken to achieve compliance with the Corporate Governance Principles. Both entities must ensure their reports reflect the effectiveness of their governance frameworks in promoting compliance, with appropriate supporting details as required [#TGT:5c3c0f6f-29a7-4b86-b0fe-109213900f3e] and permitted [#SRC:2d67e3e8-d385-4fc8-aff1-487611d02cca].

### Source passage

General. The annual report required under Rule 9.2.10 must include a statement by the Board of Directors (the "Board"), stating whether or not, in its opinion, the Corporate Governance framework of the Reporting Entity is effective in achieving the outcome required by section 73 of the FSMR and promoting compliance with the Principles, with supporting information and assumptions, and qualifications if necessary. As the Principles are the core of the Corporate Governance framework, the way in which they are applied should be the central question for the Board as it determines how the Reporting Entity conducts its affairs under its directorship in accordance with the letter and spirit of the applicable requirements including the Principles and the standards.

### Target passage

Annual reporting on compliance. The annual financial report of a Listed Entity to which this section applies must: (1) state whether the best practice standards specified in APP 4 (the "Corporate Governance Principles") have been adopted by the Listed Entity; (2) if the best practice standards in APP 4 have not been fully adopted or have been only partially adopted explain: (a) why the best practice standards were not adopted fully or adopted only partially, as is relevant; and (b) what actions, if any, have been taken by the Listed Entity to achieve compliance with the Corporate Governance Principles to the extent the relevant best practice standards were not adopted, or were only partially adopted; and (3) include a statement by Directors whether or not, in their opinion, the Corporate Governance framework of the Listed Entity is effective in promoting compliance with the Corporate Governance Principles, with supporting information and assumptions, and qualifications if necessary.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `annual report required`
- Citation hook: `9.2.10`
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
- Methods with good answer: **5 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 15: SCHEMA — test

*persona: **basic** · reference_type: **External***

**QA ID:** `4fcdcaf3-cbb7-4736-a00c-01701e0e882e`

### Question

Who is considered an 'Insider' if they have Inside Information because of their job or role in a Reporting Entity or Issuer of Financial Instruments?

### Expected answer

An 'Insider' is someone who has Inside Information under certain conditions. This includes people who get this information because they are part of the management or supervisory body of a Reporting Entity or an Issuer of Financial Instruments. It also includes those who hold shares in these entities, have access to the information through their job, or get it through illegal activities. Additionally, if someone gets the information by other means and knows, or should know, it is Inside Information, they are also considered an Insider. This definition is important because it helps determine who has special access to information that could affect financial markets, and it outlines their responsibilities and what they can or cannot do with that information [#SRC:927dee34-d53d-4ff7-90ef-042863f93509] and [#TGT:7968fd15-b5dd-45db-a02c-a941c690df86].

### Source passage

The term "Insider" is defined in section 94 as meaning: "...any person who has Inside Information: (a) as a result of his membership of an administrative, management or supervisory body of an Issuer of Financial Instruments; (b) as a result of his holding in the capital of an Issuer of Financial Instruments; (c) as a result of having access to the information through the exercise of his employment, profession or duties; (d) as a result of his criminal activities; or (e) which he has obtained by other means and which he knows, or could reasonably be expected to know, is Inside Information."

### Target passage

Insiders For the purposes of this Part, an Insider is any person who has Inside Information— (a) as a result of his membership of an administrative, management or supervisory body of a Reporting Entity or an Issuer of Financial Instruments; (b) as a result of his holding in the capital of a Reporting Entity or an Issuer of Financial Instruments; (c) as a result of having access to the information through the exercise of his employment, profession or duties; (d) as a result of his criminal activities; or (e) which he has obtained by other means and which he knows, or could reasonably be expected to know, is Inside Information.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `The term "Insider" is defined`
- Citation hook: `94`
- Source item type: `Definition`
- Target item type: `Definition`
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
- Methods with good answer: **4 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, BM25, BM25_E5_RERANK, E5
- Retrievers failing thresholds: HYBRID_RRF


---

## QA 16: SCHEMA — train

*persona: **professional** · reference_type: **External***

**QA ID:** `d011ec90-1092-496c-b5eb-6125a61d6abb`

### Question

Under what conditions may the Regulator modify requirements for an Exempt Offeror wishing to comply with Listing Rules, given that a Recognised Investment Exchange shall not permit trading of Securities unless they are admitted to the Official List?

### Expected answer

The Regulator has the authority to modify one or more requirements for an Exempt Offeror who seeks to voluntarily comply with the Listing Rules to have its Securities included on the Official List. This modification is crucial because, without it, an Exempt Offeror cannot have its Securities included in the Official List, which is a prerequisite for trading on a Recognised Investment Exchange. The prohibition is clear: a Recognised Investment Exchange shall not permit trading of Securities on its facilities unless those Securities are admitted to, and not suspended from, the Official List. This prohibition stands unless otherwise prescribed in the Rules made by the Regulator. Therefore, the Regulator's ability to modify requirements is essential for Exempt Offerors aiming to meet the conditions necessary for their Securities to be traded on a Recognised Investment Exchange [#SRC:46cdf9d3-2ae0-4bc2-8b02-87f68e832ddc] [#TGT:76d81d0b-f659-47be-bcb8-a99a24187cac].

### Source passage

The Regulator may also modify one or more requirements of this chapter for an Exempt Offeror who wishes to voluntarily comply with the Listing Rules in order to include its Securities on the Official List and thereby seek admission to trading on a Recognised Investment Exchange. Without such a modification an Exempt Offeror cannot have its Securities included in the Official List. This is because section 50(3) of the FSMR requires that a Recognised Investment Exchange shall not permit trading of Securities on its facilities unless those Securities are admitted to, and not suspended from, the Official List.

### Target passage

A Recognised Investment Exchange shall not permit trading of Securities on its facilities unless those Securities are admitted to, and not suspended from, the Official List except where otherwise prescribed in the Rules made by the Regulator.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `modify one or more requirements`
- Citation hook: `50(3)`
- Source item type: `Permission`
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
- Methods with good answer: **5 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 17: SCHEMA — train

*persona: **basic** · reference_type: **Internal***

**QA ID:** `b9c2cbf1-502a-4e8d-894b-de3433733ebc`

### Question

If a Petroleum Reporting Entity doesn't follow a non-mandatory rule in the Petroleum Reporting Standard, what must it do in its report, and what does the Regulator expect?

### Expected answer

When a Petroleum Reporting Entity does not follow a non-mandatory rule in the Petroleum Reporting Standard, it must include a statement in its report explaining how and why it didn't meet the rule. The Regulator expects that these entities either fully follow all non-mandatory rules or explain why they didn't. This requirement helps ensure that even if a rule isn't mandatory, the entity still needs to address it by either complying or explaining the reasons for not doing so. This approach by the Regulator ensures that all parts of the Petroleum Reporting Standard are considered, making the reporting process more transparent and accountable [#SRC:6604c89d-d79d-4a33-a77b-016d323c54fe] and [#TGT:47846bb1-a202-44c7-a042-465e8cf38dc6].

### Source passage

Rule 12.2.1(1) requires a Petroleum Reporting Entity to fully comply with all binding requirements set out in the Petroleum Reporting Standard (including any tables, appendices or schedules). The Regulator also expects a Petroleum Reporting Entity to fully comply with all non-mandatory requirements set out in the Petroleum Reporting Standard, or explain their non-compliance in accordance with Rule 12.2.2.

### Target passage

Requirements for all disclosures. Where a disclosure by a Petroleum Reporting Entity does not meet a non-mandatory requirement contained in the Petroleum Reporting Standard, the Petroleum Reporting Entity must provide in its disclosure a statement as to how and why its disclosure differs from the non-mandatory requirement contained in the relevant Petroleum Reporting Standard.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `explain their non-compliance in accordance`
- Citation hook: `12.2.2`
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
- Methods with good answer: **5 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 18: SCHEMA — train

*persona: **basic** · reference_type: **Internal***

**QA ID:** `61ab2856-4737-4408-b90b-f5901831b6bd`

### Question

If Authorised Persons are looking at how to treat loans that are late, what must they not do when refinancing these loans?

### Expected answer

When Authorised Persons are considering how to treat loans that are late, they must not refinance these loans in a way that changes their classification to a higher category. This means that if a loan is already classified as impaired, it cannot be refinanced to make it look like a standard or special mention credit. The rule is in place to ensure that the true status of the loan is reflected accurately and not artificially improved. Loans that are late for a certain number of days are classified into categories like special mention, substandard, doubtful, and loss. The refinancing process should respect these classifications and not attempt to elevate the credit category through Evergreening exercises. This ensures that the credit status remains transparent and truthful [#TGT:fc4bcf60-fc4a-4cd8-9848-a2bbcaaef228] as required [#SRC:2dd83781-93a2-4d56-a3fc-bf4665f983d5].

### Source passage

With respect to the ratings above, Authorised Persons should consider the following Exposures as being classified: (i) special mention; (ii) substandard; (iii) doubtful; and (iv) loss where the loans are contractually in arrears for a minimum number of days of 30, 60, 90 120 and 120 180 days respectively. Authorised Persons should also consider the treatments as set out in Rule 4.5.7 (Evergreening).

### Target passage

Any Evergreening exercise involving refinancing of past due credits must not result in their being classified as a higher category. In particular, impaired credits cannot be refinanced with the aim of classifying them as standard or special mention credits.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `consider the treatments as set out`
- Citation hook: `4.5.7`
- Source item type: `Procedure`
- Target item type: `Prohibition`
- Answer spans: 1 span(s) annotated

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **9** (0–10)
- Subscores: correctness=4, dual_use=3, realism=2

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
- Methods with good answer: **4 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, BM25_E5_RERANK, E5, HYBRID_RRF
- Retrievers failing thresholds: BM25


---

## QA 19: SCHEMA — train

*persona: **basic** · reference_type: **Internal***

**QA ID:** `8790ad83-e26f-47b3-98c6-a3e6e405fbc2`

### Question

What do Domestic Firms need to do to make sure they can pay their debts on time, considering both liquidity and capital resources?

### Expected answer

Domestic Firms, which are Authorised Persons, need to keep enough capital resources at all times, as specified by the rules, to ensure they can pay their debts when they are due. This involves having the right types and amounts of capital resources. Additionally, they must have extra capital and liquid assets that match the nature, size, and complexity of their business. This helps make sure there is no significant risk of not being able to meet liabilities. To manage liquidity, firms can hold enough cash or assets that can be quickly sold, plan their cashflows to match future needs, or borrow more if necessary. These steps help ensure that the firm can meet its financial obligations on time, fulfilling both liquidity and capital resource requirements [#SRC:456ed7d2-778d-4597-862e-2c4582c20c87] and [#TGT:afbb9f59-2c26-47f6-ac38-4c36ecd40d56].

### Source passage

In accordance with Rule 3.2.2 or Rule 3.2.4, an Authorised Person is required to ensure that there is no significant risk that liabilities cannot be met as they fall due. With specific reference to liquidity, an Authorised Person may meet its obligations in a number of ways, including: a. by holding sufficient immediately available cash or readily marketable assets; b. by securing an appropriate matching future profile of cashflows; and c. by further borrowing.

### Target passage

Domestic Firms – maintaining capital resources. An Authorised Person that is a Domestic Firm must: (a) have and maintain, at all times, Capital Resources of the types and amounts specified in, and calculated in accordance with, these Rules; (b) ensure that it maintains capital and liquid assets in addition to the requirement in (a) which are adequate in relation to the nature, size and complexity of its business to ensure that there is no significant risk that liabilities cannot be met as they fall due.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `no significant risk that liabilities cannot be met`
- Citation hook: `3.2.4`
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
- Methods retrieving all relevant in top-10: **0** / 5
- High concordance (hit-any): **True**
- Low concordance (hit-any): **False**
- Retrievers with ≥1 relevant: bge.txt, bm25.txt, bm25_e5_rerank.txt, e5.txt, hybrid_rrf_bm25_e5.txt

**Answer quality / RAG concordance:**
- Methods with good answer: **5 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 20: SCHEMA — train

*persona: **professional** · reference_type: **Internal***

**QA ID:** `3a1b1b74-d606-4207-91b3-0d9ddb22f624`

### Question

How must an Authorised Person, acting as both a Money Remitter and a Payment Account Provider, calculate its overall Variable Capital Requirement, considering the necessary steps and calculations?

### Expected answer

An Authorised Person who functions as both a Money Remitter and a Payment Account Provider is required to calculate its overall Variable Capital Requirement by aggregating the monthly payment volumes for both activities. This involves following a specific calculation procedure. The Payment Account Provider must determine the Variable Capital Requirement by summing up percentages of different tiers of monthly payment volumes: 2.5% of the first $10 million, 1% of the next $90 million, 0.5% of the subsequent $150 million, and 0.25% of any remaining volume. This structured approach ensures that the capital requirement reflects the scale of the payment activities undertaken by the Authorised Person, thereby aligning with regulatory expectations [#SRC:b68ce9bd-b816-410b-92f6-32569f63a223] and ensuring compliance with the procedural guidelines [#TGT:7593338e-8695-47bb-ad6a-b441de562eb4].

### Source passage

An Authorised Person acting as both a Money Remitter and a Payment Account Provider must calculate its overall Variable Capital Requirement for the related activities by adding together the monthly payment volumes for those activities and undertaking the calculation in Rule 3.6A.4.

### Target passage

Payment Account Providers. A Payment Account Provider must calculate its Variable Capital Requirement as the sum of the following: (a) 2.5% of the first $10 million of monthly payment volume; (b) 1% of the next $90 million of monthly payment volume; (c) 0.5% of the next $150 million of monthly payment volume; and (d) 0.25% of any remaining monthly payment volume.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `calculate its overall Variable Capital Requirement`
- Citation hook: `3.6A.4`
- Source item type: `Obligation`
- Target item type: `Procedure`
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
- Methods with good answer: **4 / 5**
- High concordance on answer quality: **True**
- Low concordance on answer quality: **False**
- Retrievers passing thresholds: BGE, BM25_E5_RERANK, E5, HYBRID_RRF
- Retrievers failing thresholds: BM25


---

