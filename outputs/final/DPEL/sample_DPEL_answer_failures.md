# RegRAG-Xref sampled QAs

_Source file: `sample_DPEL_answer_failures.jsonl`_

## QA 1: DPEL — n/a

*persona: **basic** · reference_type: **External***

**QA ID:** `4e2aa127-f652-422c-a8b7-f6c972dc9e7d`

### Question

If a Mining Reporting Entity thinks some economic assumptions are sensitive, what should it do when sharing forecast financial information, and what if it is also giving out a Prospectus in ADGM?

### Expected answer

A Mining Reporting Entity must share all important economic assumptions for forecast financial information, even if they are sensitive [#SRC:2c78a258-d9f2-4150-9d2c-ba681d8f9489]. If the assumptions are sensitive, the entity should say so and explain how they were decided [#SRC:2c78a258-d9f2-4150-9d2c-ba681d8f9489]. When also giving out a Prospectus in ADGM, the entity needs to include all information that investors need to make informed choices, as required by section 62(1) of FSMR [#TGT:8597f744-9885-4eb3-9d70-e86ac02e5856]. This means balancing sensitive information with the need for full disclosure in the Prospectus.

### Source passage

A Mining Reporting Entitys disclosure pursuant to Rule 11.9.1 must include: (1) in relation to the assumptions used to determine the forecast financial information: (a) all material economic assumptions employed; (b) if the Mining Reporting Entity considers the material economic assumptions to be commercially sensitive, a statement to that effect and an explanation of the methodology used to determine the material economic assumptions; and Guidance A Mining Reporting Entity that considers certain information relating to the material economic assumptions to be commercially sensitive should refer to paragraphs 47-54 of the Guidance on Mining and paragraphs 127 and 128 of the Guidance on Continuous Disclosure. (c) all other material assumptions utilised. (2) the Production Target from which the forecast financial information is derived (including all the information contained in Rule 11.8.3).

### Target passage

ORE RESERVES . The FSRA does expect a Mining Reporting Entity to have to disclose commercially sensitive information (e.g., pricing or volumes under long term contractual commitments) to meet this Rule obligation. A Mining Reporting Entity (and other relevant entities) may, however, have to carefully consider whether this information needs to be disclosed to meet other disclosure requirements, including in reference to: a) where an Issuer is issuing a Prospectus within ADGM, and the requirement in section 62(1) of FSMR to include all information that investors would reasonably require and expect to find in a Prospectus for the purposes of making an informed investment decision; or b) the requirements in sections 95(2) of FSMR and Rule 7.2.1 to disclose information that ‘would, if generally available, be likely to have a significant effect on the price…’ of Financial Instruments.

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
- Methods with good answer: **0 / 5**
- High concordance on answer quality: **False**
- Low concordance on answer quality: **True**
- Retrievers failing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 2: DPEL — n/a

*persona: **professional** · reference_type: **Internal***

**QA ID:** `ec432d46-e41f-4d83-8d2a-e325bd9b96be`

### Question

What due diligence must a Recognised Investment Exchange perform when admitting a Financial Instrument that references a benchmark provided by a Price Reporting Agency, and what specific requirements must the Price Reporting Agency meet under Rule 3.11.2?

### Expected answer

A Recognised Investment Exchange must conduct appropriate due diligence to ensure that a Price Reporting Agency meets the requirements specified in Rule 3.11.2 when admitting a Financial Instrument that references a benchmark provided by the agency [#SRC:69082061-a103-4087-acae-fa41e87fd0da]. The Price Reporting Agency must have fair and non-discriminatory procedures for price establishment, ensure transparency in its methodology, prioritize concluded transactions where appropriate, maintain good standing and independence, have a sound corporate governance framework, avoid conflicts of interest, and provide adequate complaint resolution mechanisms [#TGT:8a81e6cb-f1f1-4988-af97-f966f288017a].

### Source passage

When admitting to trading a Financial Instrument that references an underlying benchmark or index provided by a Price Reporting Agency, a Recognised Investment Exchange must undertake appropriate due diligence to ensure that the Price Reporting Agency meets the requirements in Rule 3.11.2.

### Target passage

For the purposes of Rules 3.11.1 and 3.11.3, a Price Reporting Agency must: (a) have fair and non-discriminatory procedures for establishing prices of a Financial Instrument, which are made public; (b) demonstrate adequate and appropriate transparency over the methodology, calculation and inputs to allow users to understand how the benchmark or index is derived and its potential limitations; (c) where appropriate, give priority to concluded transactions in making assessments and adopt measures to minimise selective reporting; (d) be of good standing and repute as an independent and objective price reporting agency or index provider; (e) have a sound corporate governance framework; (f) have adequate arrangements to avoid its staff having any conflicts of interest where such conflicts are, or are likely to have, a material adverse impact on a price establishment process; and (g) adequate complaint resolution mechanisms to resolve any complaints about its assessment process and methodology.

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
- Methods with good answer: **0 / 5**
- High concordance on answer quality: **False**
- Low concordance on answer quality: **True**
- Retrievers failing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 3: DPEL — n/a

*persona: **basic** · reference_type: **Internal***

**QA ID:** `1efd8486-7db0-4f8d-8b37-70616af0e3f9`

### Question

If a Fund Manager changes the Prospectus for a Passported Fund, what must they do to notify the Regulator, and what form should this take?

### Expected answer

The Fund Manager must tell the Regulator as soon as possible, and no later than seven days after they know about the change, if the Prospectus for a Passported Fund is changed [#TGT:7a51b100-c0e6-41bd-809c-d2ae395a9898]. They need to include details of what happened and a copy of the new Prospectus in the notification, which must be in the form the Regulator says to use [#SRC:a293c037-9b5d-4128-8318-f840f0264d1f].

### Source passage

The notification referred to in Rule 6.6.2 must be in such prescribed form as the Regulator may direct from time to time. At a minimum, the notification must be accompanied by reasonable detail of the event and (where the Prospectus has been amended or replaced) a copy of the new Prospectus.

### Target passage

The Fund Manager of a Passported Fund must notify the Regulator as soon as practicable of any material events, in accordance with applicable ADGM legislation. In particular (but without limitation), a Fund Manager or the governing body or trustee of a Passported Fund must notify the Regulator as soon as practicable (and in any case no later than seven days after it becomes aware) of any of the following events: (a) the Fund Manager intends to retire as manager of the Passported Fund; (b) it is proposed that a successor manager will be appointed in relation to the Passported Fund; (c) the Fund Manager has been removed or replaced as manager of the Passported Fund; (d) any material service provider to the Passported Fund (including, without limitation, any custodian) or an Agent or Licensed Person resigns, is appointed, is removed, or is replaced; (e) the Prospectus relating to the Passported Fund has been amended or replaced; (f) winding-up of the Passported Fund has commenced; or (g) the Fund Manager intends to vary or revoke its Financial Service Permission (or any conditions contained in that Financial Service Permission).

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
- Methods with good answer: **0 / 5**
- High concordance on answer quality: **False**
- Low concordance on answer quality: **True**
- Retrievers failing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 4: DPEL — n/a

*persona: **professional** · reference_type: **External***

**QA ID:** `f57e8776-ef5f-4178-ba0d-e615f6a3c56a`

### Question

What are the requirements for an Authorised Person conducting a Regulated Activity in relation to Virtual Assets within ADGM, and how does the FSRA's power influence these activities?

### Expected answer

An Authorised Person conducting a Regulated Activity in relation to Virtual Assets within ADGM is required to use only Accepted Virtual Assets [#TGT:7bed5f55-c0d5-4a97-93d4-3db078c11610]. The FSRA holds the authority to determine which Virtual Assets are classified as Accepted Virtual Assets, thereby influencing which assets can be used by Authorised Persons to prevent engagement in potentially higher-risk activities associated with illiquid or immature Virtual Assets [#SRC:e21bdb20-ef7f-4b2d-8f20-e448b1576e78].

### Source passage

REGULATORY REQUIREMENTS FOR AUTHORISED PERSONS ENGAGED IN REGULATED ACTIVITIES IN RELATION TO VIRTUAL ASSETS Accepted Virtual Assets COBS Rule 17.2.1 permits an Authorised Person to conduct a Regulated Activity in relation to Accepted Virtual Assets only. The FSRA has a general power to determine each Accepted Virtual Asset that will be permitted to be used by an Authorised Person within ADGM, in order to prevent potential higher-risk activities relating to illiquid or immature Virtual Assets.

### Target passage

An Authorised Person conducting a Regulated Activity in relation to Virtual Assets must only use Accepted Virtual Assets.

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
- Methods with good answer: **0 / 5**
- High concordance on answer quality: **False**
- Low concordance on answer quality: **True**
- Retrievers failing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 5: DPEL — n/a

*persona: **professional** · reference_type: **External***

**QA ID:** `c0f72d68-0dd7-4491-9086-581f2991fcc5`

### Question

How is the definition of 'Insider' differentiated between a Reporting Entity and an Issuer of Financial Instruments, and what are the implications for individuals with Inside Information obtained through criminal activities?

### Expected answer

The definition of 'Insider' includes any person with Inside Information due to their role in an administrative, management, or supervisory body, or their capital holding, applicable to both a Reporting Entity and an Issuer of Financial Instruments [#TGT:7968fd15-b5dd-45db-a02c-a941c690df86]. However, the SOURCE text specifically mentions only an Issuer of Financial Instruments, not a Reporting Entity, indicating a narrower scope [#SRC:927dee34-d53d-4ff7-90ef-042863f93509]. For individuals obtaining Inside Information through criminal activities, both passages agree that such individuals are considered Insiders, emphasizing the importance of the means by which the information is acquired [#SRC:927dee34-d53d-4ff7-90ef-042863f93509][#TGT:7968fd15-b5dd-45db-a02c-a941c690df86].

### Source passage

The term "Insider" is defined in section 94 as meaning: "...any person who has Inside Information: (a) as a result of his membership of an administrative, management or supervisory body of an Issuer of Financial Instruments; (b) as a result of his holding in the capital of an Issuer of Financial Instruments; (c) as a result of having access to the information through the exercise of his employment, profession or duties; (d) as a result of his criminal activities; or (e) which he has obtained by other means and which he knows, or could reasonably be expected to know, is Inside Information."

### Target passage

Insiders For the purposes of this Part, an Insider is any person who has Inside Information— (a) as a result of his membership of an administrative, management or supervisory body of a Reporting Entity or an Issuer of Financial Instruments; (b) as a result of his holding in the capital of a Reporting Entity or an Issuer of Financial Instruments; (c) as a result of having access to the information through the exercise of his employment, profession or duties; (d) as a result of his criminal activities; or (e) which he has obtained by other means and which he knows, or could reasonably be expected to know, is Inside Information.

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

## QA 6: DPEL — n/a

*persona: **professional** · reference_type: **Internal***

**QA ID:** `5ddc629d-1c2e-4e5e-bf30-590d0aee153d`

### Question

Under what conditions may a Customer and a Third Party Provider agree in writing to exclude specific rules, and how does this relate to the Third Party Provider's liability for unauthorised transactions?

### Expected answer

A Customer who is not a Natural Person and a Third Party Provider may agree in writing to exclude certain rules, such as those related to charges for information, withdrawal of consent, and revocation of a Payment Order, among others [#SRC:10510c2c-99d3-4cba-bac5-61cda5d00d44]. This agreement can also specify a different time period for unauthorised or incorrectly executed Payment Transactions [#SRC:10510c2c-99d3-4cba-bac5-61cda5d00d44]. However, the Third Party Provider remains liable to its Customer for any charges or interest resulting from non-execution, defective, or late execution of a Third Party Transaction [#TGT:e704735d-e9c8-4326-b79a-28e066317151]. Therefore, while certain rules can be excluded by mutual agreement, the liability for unauthorised transactions still holds.

### Source passage

Where the Customer is not a Natural Person, the Customer and the Third Party Provider may agree in writing that the following Rules do not apply: (a) Rules 20.2.15 and 20.2.16 (charges for information); (b) Rule 20.7.3 and 20.7.4 (withdrawal of consent); (c) Rule 20.8.2 (revocation of a Payment Order); (d) Rules 20.10.1 and 20.10.2 (requests for refund); (e) Rule 20.11.1 (evidence on authentication and execution); (f) Rule 20.12.5 (liability for charges); and the parties may agree that a different time period applies concerning unauthorised or incorrectly executed Payment Transactions for the purposes of Rule 20.10.1.

### Target passage

Third Party Provider’s liability for unauthorised Third Party Transactions. A Third Party Provider is liable to its Customer for any charges for which the Customer is responsible and any interest which the Customer must pay as a consequence of the non-execution, defective or late execution of a Third Party Transaction by the Third Party Provider.

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

## QA 7: DPEL — n/a

*persona: **basic** · reference_type: **Internal***

**QA ID:** `27944edd-75fa-44c1-be92-caed9599452a`

### Question

When can a company issue Securities under an Employee Incentive Scheme if its Securities are already on the Official List, and what role does the Regulator's website play in this?

### Expected answer

A company can issue Securities under an Employee Incentive Scheme if, within three years before the issue, the scheme was set up before the company's Securities were listed, with details in an Approved Prospectus or lodged documents, or if the company's shareholders approved the issue as an exception to Rule 9.7.1 [#SRC:a2108df9-4a76-4d9c-8a4a-7e058e5e8113]. The Regulator's website plays a crucial role as the admission of Securities to the Official List only becomes effective when the Regulator publishes this admission on the ADGM website [#TGT:d28d3376-4af3-4b11-b90d-3f24c8e54555].

### Source passage

An issue of Securities under an Employee Incentive Scheme if within three years before the issue date: (a) in the case of a scheme established before the Listed Entitys Securities were admitted to the Official List a summary of the terms of the scheme and the maximum number of Equity Securities proposed to be issued under the scheme were set out in in its Approved Prospectus or documents lodged with the Regulator under Rule 2.4.3; or (b) the holders of the Listed Entitys Ordinary Securities have approved the issue of Equity Securities under the scheme as an exception to Rule 9.7.1. The notice of meeting must have included: (i) a summary of the terms of the scheme; (ii) the number of Securities issued under the scheme since the Listed Entitys Securities were admitted to the Official List, or the date of the last approval under this Rule; and (iii) the maximum number of Equity Securities proposed to be issued under the scheme following the approval.

### Target passage

Listing application. An admission of Securities to the Official List becomes effective only when the Regulator has published the admission by adding such Securities to the Official List on the ADGM website.

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
- Retrievers with all relevant: bm25.txt, bm25_e5_rerank.txt, e5.txt, hybrid_rrf_bm25_e5.txt

**Answer quality / RAG concordance:**
- Methods with good answer: **0 / 5**
- High concordance on answer quality: **False**
- Low concordance on answer quality: **True**
- Retrievers failing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 8: DPEL — n/a

*persona: **basic** · reference_type: **External***

**QA ID:** `859902f3-2d20-489d-bd24-5cecc8fe38b4`

### Question

When can someone avoid being sued for false information in a Prospectus, and how does this connect to having to pay for losses because of wrong details in the Prospectus?

### Expected answer

Someone can avoid being sued for false information in a Prospectus if they meet any of the specific conditions listed in section 70(2) to (6) of the FSMR [#SRC:4bab6b81-d4ed-4745-b082-99a3161debe0]. However, the Rules made by the Regulator say that a person responsible for a Prospectus must pay for losses if someone buys Securities and loses money because of wrong or missing details in the Prospectus [#TGT:06cd3b51-1068-4851-9420-1345002addac]. So, even if someone avoids being sued under the FSMR, they might still have to pay for losses unless they meet those specific conditions.

### Source passage

Pursuant to section 70(1) of the FSMR, a Person is hereby prescribed as not incurring civil liability for any loss arising from any false, misleading, or deceptive statement or omission in a Prospectus if any of the circumstances specified in (2) to (6) apply.

### Target passage

Any person prescribed in the Rules made by the Regulator as being liable for a Prospectus is liable to pay compensation to another person who has acquired Securities to which the Prospectus relates and who has suffered loss or damage arising from any untrue or misleading statement in the Prospectus or the omission from it of any material matter required to have been included in the Prospectus by or under these Regulations.

**LLM-as-judge summary:**
- Fused passed: **True**
- Fused score: **9** (0–10)
- Subscores: correctness=4, dual_use=4, realism=2

**IR retrieval concordance:**
- Number of relevant passages (qrels): **2**
- Evaluated at top-10 per retriever
- Methods hitting ≥1 relevant in top-10: **5** / 5
- Methods retrieving all relevant in top-10: **2** / 5
- High concordance (hit-any): **True**
- Low concordance (hit-any): **False**
- Retrievers with ≥1 relevant: bge.txt, bm25.txt, bm25_e5_rerank.txt, e5.txt, hybrid_rrf_bm25_e5.txt
- Retrievers with all relevant: bm25_e5_rerank.txt, hybrid_rrf_bm25_e5.txt

**Answer quality / RAG concordance:**
- Methods with good answer: **0 / 5**
- High concordance on answer quality: **False**
- Low concordance on answer quality: **True**
- Retrievers failing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 9: DPEL — n/a

*persona: **basic** · reference_type: **Internal***

**QA ID:** `240f4a2d-0cd2-43e7-b350-bb28f8f4d5bc`

### Question

If a Customer is not a Natural Person, when can they agree with a Third Party Provider to ignore Rule 20.8.2, and what does this mean for stopping a Third Party Transaction?

### Expected answer

A Customer who is not a Natural Person can agree with a Third Party Provider to ignore Rule 20.8.2 if they put it in writing [#SRC:10510c2c-99d3-4cba-bac5-61cda5d00d44]. Rule 20.8.2 deals with when a Payment Order can be revoked. Normally, a Customer can stop a Third Party Transaction before it reaches a point where it can't be revoked anymore [#TGT:84c622c5-b22e-4360-9f94-1bd99e99f12c]. If they agree to ignore this rule, they might set different terms for when they can stop a transaction.

### Source passage

Where the Customer is not a Natural Person, the Customer and the Third Party Provider may agree in writing that the following Rules do not apply: (a) Rules 20.2.15 and 20.2.16 (charges for information); (b) Rule 20.7.3 and 20.7.4 (withdrawal of consent); (c) Rule 20.8.2 (revocation of a Payment Order); (d) Rules 20.10.1 and 20.10.2 (requests for refund); (e) Rule 20.11.1 (evidence on authentication and execution); (f) Rule 20.12.5 (liability for charges); and the parties may agree that a different time period applies concerning unauthorised or incorrectly executed Payment Transactions for the purposes of Rule 20.10.1.

### Target passage

The Customer may withdraw its consent to an individual Third Party Transaction at any time before the point at which the Third Party Transaction can no longer be revoked as set out in Rule 20.8.2.

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
- Retrievers with all relevant: bm25.txt, bm25_e5_rerank.txt, e5.txt, hybrid_rrf_bm25_e5.txt

**Answer quality / RAG concordance:**
- Methods with good answer: **0 / 5**
- High concordance on answer quality: **False**
- Low concordance on answer quality: **True**
- Retrievers failing thresholds: BGE, BM25, BM25_E5_RERANK, E5, HYBRID_RRF


---

## QA 10: DPEL — n/a

*persona: **basic** · reference_type: **Internal***

**QA ID:** `0355529c-382c-4e04-9b15-b2d06a743b3d`

### Question

If a company doesn't fully follow the best practice standards in APP 4, what must it explain in its annual report and Prospectus?

### Expected answer

If a company does not fully follow the best practice standards in APP 4, it must explain in its Prospectus why it didn't adopt these standards fully and what other measures it took to meet the Corporate Governance Principles [#SRC:ff5bac8d-3dc7-46dd-a9ce-b0c32a42422e]. In its annual report, the company must also state whether it adopted the APP 4 standards, explain any non-adoption, and describe actions taken to comply with the Corporate Governance Principles [#TGT:5c3c0f6f-29a7-4b86-b0fe-109213900f3e].

### Source passage

Generally, if a Reporting Entity does not adopt the best practice standards set out in APP 4, or adopts them only partially, the Regulator would expect the reasons for doing so and any alternative measures adopted to achieve the outcomes intended by the Corporate Governance Principles to be disclosed in the Prospectus and thereafter pursuant to the Disclosure required under Rule 9.2.10. Any inaccurate or false representations would lead to the imposition of civil liability in accordance with section 70 of the FSMR.

### Target passage

Annual reporting on compliance. The annual financial report of a Listed Entity to which this section applies must: (1) state whether the best practice standards specified in APP 4 (the "Corporate Governance Principles") have been adopted by the Listed Entity; (2) if the best practice standards in APP 4 have not been fully adopted or have been only partially adopted explain: (a) why the best practice standards were not adopted fully or adopted only partially, as is relevant; and (b) what actions, if any, have been taken by the Listed Entity to achieve compliance with the Corporate Governance Principles to the extent the relevant best practice standards were not adopted, or were only partially adopted; and (3) include a statement by Directors whether or not, in their opinion, the Corporate Governance framework of the Listed Entity is effective in promoting compliance with the Corporate Governance Principles, with supporting information and assumptions, and qualifications if necessary.

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
- Methods with good answer: **1 / 5**
- High concordance on answer quality: **False**
- Low concordance on answer quality: **True**
- Retrievers passing thresholds: HYBRID_RRF
- Retrievers failing thresholds: BGE, BM25, BM25_E5_RERANK, E5


---

