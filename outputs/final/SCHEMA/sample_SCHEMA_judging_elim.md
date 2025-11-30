# RegRAG-Xref sampled QAs

_Source file: `sample_SCHEMA_judging_elim.jsonl`_

## QA 1: SCHEMA — eliminated

*persona: **basic** · reference_type: **External***

**QA ID:** `00124ef1-94b7-4a63-a21f-67f6296c0dcd`

### Question

When can the Regulator refuse a listing application or set conditions for admitting Securities to the Official List?

### Expected answer

The Regulator can refuse a listing application or set conditions for admitting Securities to the Official List when certain conditions are met. This means that if the Regulator finds it necessary, they can either stop a Security from being listed or allow it with specific rules attached. These actions help ensure that all Securities on the Official List meet the required standards and protect investors. The Regulator's ability to impose, change, or remove these conditions is important for keeping the market stable and trustworthy. By having the power to refuse an application or impose conditions, the Regulator can make sure that only Securities that follow the rules are listed. This approach helps maintain the quality and reliability of the Official List, which is crucial for investor confidence and market integrity [#SRC:790f04b5-f8da-46cb-9014-cff27cdb7226] as specified [#TGT:764bd3fc-ac8b-451f-b8bb-aa931a00c48b].

### Source passage

Under section 52(1)(b) of the FSMR, the Regulator may impose conditions or restrictions in respect of the admission of Securities to the Official List, or vary or withdraw such conditions or restrictions.

### Target passage

The Regulator may— (a) refuse an Application for Listing; or (b) impose conditions or restrictions, in respect of the admission of Securities to the Official List, or vary or withdraw such conditions or restrictions; in the circumstances specified in subsection ‎(2).

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `impose conditions or restrictions`
- Citation hook: `52(1)(b)`
- Source item type: `Permission`
- Target item type: `Permission`
- Answer spans: 1 span(s) annotated

**LLM-as-judge summary:**
- Fused passed: **False**
- Fused score: **6** (0–10)
- Subscores: correctness=2, dual_use=3, realism=2


---

## QA 2: SCHEMA — eliminated

*persona: **professional** · reference_type: **Internal***

**QA ID:** `886f8550-634b-4d32-a896-b43b59bf00a1`

### Question

When an Authorised Person operates an MTF or OTF, how shall references to Financial Instruments in COBS Rule 8.2.1 be interpreted, and what specific obligations must they fulfill under the MIR rulebook?

### Expected answer

In the context of operating a Multilateral Trading Facility (MTF) or an Organised Trading Facility (OTF), an Authorised Person must interpret references to Financial Instruments in COBS Rule 8.2.1 as Virtual Assets. This reinterpretation aligns with the broader regulatory framework that governs such activities. Additionally, these operators must adhere to specific obligations outlined in the MIR rulebook, which are typically applicable to Recognised Bodies or Recognised Investment Exchanges. These obligations include maintaining operational systems and controls, ensuring proper transaction recording, meeting membership criteria, preventing financial crime and market abuse, adhering to rules and consultation processes, and ensuring fair and orderly trading. Furthermore, they must comply with pre-trade and post-trade transparency obligations, public disclosure requirements, settlement and clearing services, default rules, and the use of Price Reporting Agencies. These comprehensive requirements ensure that MTF and OTF operators maintain high standards of operation and transparency in the trading of Virtual Assets, thereby aligning with the regulatory expectations set forth in both COBS and MIR [#SRC:a3736367-db02-465d-809f-1bc6cfd7bbcd] and [#TGT:180edda8-db12-4969-97d5-182435bdf094].

### Source passage

For the purposes of Rule 17.7.2, the following references in COBS, Chapter 8 should be read as follows: (a) references to Investment or Investments shall be read as references to Virtual Asset or Virtual Assets, as applicable; and (b) references to Financial Instrument or Financial Instruments (including those in MIR as incorporated by virtue of COBS Rule 8.2.1) shall be read as references to Virtual Asset or Virtual Assets, as applicable.

### Target passage

In addition to the general requirements applicable to Authorised Persons in COBS, GEN and elsewhere in the Rules, an Authorised Person carrying on the Regulated Activity of Operating an MTF (an "MTF Operator") or an Authorised Person carrying on the Regulated Activity of Operating an OTF (an “OTF Operator”) must comply with the following requirements applicable to a Recognised Body or Recognised Investment Exchange set out in the MIR rulebook, reading references to Recognised Bodies or Recognised Investment Exchanges in the relevant rules as if they were references to the MTF Operator or OTF Operator: (a) MIR 2.6 (Operational systems and controls); (b) MIR 2.7.1 and 2.7.2 (Transaction recording); (c) MIR 2.8 (Membership criteria and access); (d) MIR 2.9 (Financial crime and market abuse); (e) MIR 2.11 (Rules and consultation); (f) MIR 3.3 (Fair and orderly trading); (g) MIR 3.5 (Pre-trade transparency obligations); (h) MIR 3.6 (Post-trade transparency obligations); (i) MIR 3.7 (Public disclosure); (j) MIR 3.8 (Settlement and Clearing Services); (k) MIR 3.10 (Default Rules); and (l) MIR 3.11 (Use of Price Reporting Agencies).

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `references to Financial Instrument or Financial Instruments`
- Citation hook: `8.2.1`
- Source item type: `Definition`
- Target item type: `Obligation`
- Answer spans: 1 span(s) annotated

**LLM-as-judge summary:**
- Fused passed: **False**
- Fused score: **0** (0–10)
- Subscores: correctness=0, dual_use=0, realism=0


---

## QA 3: SCHEMA — eliminated

*persona: **professional** · reference_type: **External***

**QA ID:** `b9af6d7b-9657-42da-bdb1-555cb012ef2f`

### Question

Under what circumstances may a Requirement be imposed on a firm, and how does this relate to the scope of activities covered?

### Expected answer

A Requirement may be imposed on a firm when it is necessary to ensure compliance with the regulatory framework. This imposition is not limited to the firm's Regulated Activities but can also extend to other activities as deemed necessary. The scope of such Requirements is outlined under section 35, with further provisions detailed in section 36, which clarify the extent and conditions under which these Requirements can be applied. This ensures that the regulatory body has the flexibility to address a wide range of activities that may impact the firm's compliance status. The ability to impose and vary these Requirements is crucial for maintaining regulatory oversight and ensuring that firms adhere to the necessary standards. The provisions allow for a comprehensive approach to regulation, ensuring that all relevant activities of a firm can be addressed as required [#TGT:b6bd33bc-b9b3-489d-badf-67503316e220] and permitted [#SRC:dd33d5b7-2e3a-44fc-b3da-3ec706e631e3].

### Source passage

We may impose a Requirement on a firm under section 35 of FSMR so as to require the firm to take action, or refrain from taking action, specified by us. Section 36 of FSMR sets out further provisions regarding our power to impose Requirements and provides that a Requirement can extend to a firms activities which are not Regulated Activities.

### Target passage

Imposition and variation of requirements. Requirements under section ‎35: further provisions

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `our power to impose Requirements`
- Citation hook: `36`
- Source item type: `Permission`
- Target item type: `Scope`
- Answer spans: 1 span(s) annotated

**LLM-as-judge summary:**
- Fused passed: **False**
- Fused score: **3** (0–10)
- Subscores: correctness=1, dual_use=2, realism=2


---

## QA 4: SCHEMA — eliminated

*persona: **professional** · reference_type: **External***

**QA ID:** `aafeb5a5-9cc3-4116-bc3f-639410078907`

### Question

When the Regulator exercises its powers at the request of a Non-ADGM Regulator, under what conditions may Confidential Information gathered be disclosed to that Non-ADGM Regulator?

### Expected answer

When the Regulator acts upon the request or on behalf of a Non-ADGM Regulator, it may gather Confidential Information through the exercise of its powers. The disclosure of such information is strictly regulated and can only occur in accordance with specific provisions. This ensures that any Confidential Information obtained under sections 215, 216, or 217 is disclosed to the Non-ADGM Regulator only if it aligns with the provisions outlined in sections 198 or 199 of the FSMR. This regulatory framework underscores the importance of maintaining confidentiality while facilitating cooperation, assistance, and support to Non Abu Dhabi Global Market Regulators. The scope of these actions is to ensure that the Regulator's support in investigations or other activities is conducted within a structured and legally compliant framework, thereby safeguarding sensitive information while promoting international regulatory cooperation [#SRC:1c83f212-bd45-4299-b2e1-66ed94f62623] and [#TGT:bb0aeccc-f1be-4acb-994d-4f6f37faf839].

### Source passage

If the Regulator decides to exercise its powers at the request, or on behalf, of a Non-ADGM Regulator, Confidential Information gathered as result of the Regulator exercising its powers under sections 215, 216 or 217 can only be disclosed to that Non-ADGM Regulator in accordance with the provisions of sections 198 or section 199 of the FSMR.

### Target passage

Cooperation, assistance and support to Non Abu Dhabi Global Market Regulators. Investigations etc. in support of Non Abu Dhabi Global Market Regulators

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `Confidential Information gathered as result`
- Citation hook: `217`
- Source item type: `Procedure`
- Target item type: `Scope`
- Answer spans: 1 span(s) annotated

**LLM-as-judge summary:**
- Fused passed: **False**
- Fused score: **6** (0–10)
- Subscores: correctness=2, dual_use=2, realism=2


---

## QA 5: SCHEMA — eliminated

*persona: **basic** · reference_type: **Internal***

**QA ID:** `656d7cbd-ff4b-4035-95be-798ec9b98c14`

### Question

What do Authorised Persons need to do when they handle Virtual Assets and Client Money?

### Expected answer

Authorised Persons who deal with Virtual Assets and manage Client Money must follow specific rules to ensure everything is done correctly. The rules say that when we talk about 'Investments,' it also means Virtual Assets. So, if an Authorised Person is involved in activities with Virtual Assets, they must follow the Client Money Rules found in Chapter 14. These rules are important because they help protect the money that clients trust them with. The Authorised Person has to make sure they are doing everything according to these rules, especially when they are holding or controlling Client Money. This is to ensure that the handling of Virtual Assets is as secure and regulated as traditional investments, keeping client funds safe and secure [#SRC:1a0d0b8c-b8bf-48a1-b6ab-683d17ae56a0] and [#TGT:b2806cf3-5ff8-43bc-9eb3-8d2fa28c39e0].

### Source passage

For the purposes of Rule 17.8.1 Investment or Investments, (and, a result, the corresponding references to Client Investments) shall be read as encompassing Virtual Asset or Virtual Assets, as applicable.

### Target passage

In addition to the general requirements applicable to an Authorised Person conducting a Regulated Activity in relation to Virtual Assets as set out in Rules 17.1 – 17.6, an Authorised Person that is Providing Custody in relation to Virtual Assets must comply with the requirements set out in COBS, Chapters 14, 15 and 16, as set out in Rules 17.8.2 – 17.8.3. Guidance An Authorised Person conducting a Regulated Activity in relation to Virtual Assets which hold or control Client Money must comply with the Client Money Rules set out in Chapter ‎14, as amended by the requirements set out in Rule ‎17.8.4.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `Investment or Investments shall be read as encompassing Virtual Asset`
- Citation hook: `17.8.1`
- Source item type: `Definition`
- Target item type: `Obligation`
- Answer spans: 1 span(s) annotated

**LLM-as-judge summary:**
- Fused passed: **False**
- Fused score: **6** (0–10)
- Subscores: correctness=1, dual_use=3, realism=2


---

## QA 6: SCHEMA — eliminated

*persona: **basic** · reference_type: **External***

**QA ID:** `6e37f802-f77c-4b20-889e-eac390216cf7`

### Question

When does a Mining Reporting Entity have to tell the public about changes in its production targets, and how is this linked to what counts as Inside Information?

### Expected answer

A Mining Reporting Entity must inform the public about any significant changes in its production targets if these changes could affect the price of Financial Instruments. This duty arises when the information is precise, not publicly known, and relates to the entity or the financial instruments. If such information, once public, is likely to change the price of these instruments, it meets the criteria for Inside Information. This means the entity has to decide if the changes in production targets are significant enough to require disclosure. This ensures that the market remains fair and transparent, as the information could influence trading decisions if it were generally available. The obligation to disclose is part of the rules that ensure important information is shared with the market to prevent unfair advantages [#SRC:09aca426-0526-4305-9aa4-12e87c9b3c96] and [#TGT:ac9dc52d-0e6a-4c83-b170-ffe156109977].

### Source passage

Production Targets-Disclosure requirements . If a Mining Reporting Entity becomes aware that its Production results will differ materially (up or down) from any Production Target it has disclosed, it may have a legal obligation to disclose this. This obligation to disclose may arise under Rule 7.2.1 and section 95(2) of FSMR, in order to disclose information that would, if generally available, be likely to have a significant effect on the price... of Financial Instruments.

### Target passage

In relation to Financial Instruments, Accepted Virtual Assets, Accepted Spot Commodities or Related Instruments which are not Commodity Derivatives, Inside Information is information of a Precise nature which— (a) is not generally available; (b) relates, directly or indirectly, to one or more Reporting Entities or Issuers of the Financial Instruments or to one or more of the Financial Instruments, Accepted Virtual Assets or Accepted Spot Commodities; and (c) would, if generally available, be likely to have a significant effect on the price of the Financial Instruments, Accepted Virtual Assets, Accepted Spot Commodities or Related Instruments.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `obligation to disclose may arise`
- Citation hook: `95(2)`
- Source item type: `Obligation`
- Target item type: `Definition`
- Answer spans: 1 span(s) annotated

**LLM-as-judge summary:**
- Fused passed: **False**
- Fused score: **6** (0–10)
- Subscores: correctness=3, dual_use=4, realism=2


---

## QA 7: SCHEMA — eliminated

*persona: **basic** · reference_type: **External***

**QA ID:** `ad3a3e84-7bf0-4715-9703-bc2b91122d53`

### Question

When can a Requirement be put on a firm, and what activities does it cover?

### Expected answer

A Requirement can be put on a firm when the regulatory body decides it is necessary to make sure the firm follows the rules. This isn't just about the firm's main regulated activities; it can also include other activities that might affect compliance. The rules about this are in section 35, with more details in section 36, explaining how and when these Requirements can be used. This helps the regulators make sure that firms are doing what they need to do to stay in line with the rules. By being able to impose and change these Requirements, the regulators can keep a close watch on all the firm's activities, not just the ones that are officially regulated. This approach helps ensure that firms are meeting all necessary standards as required [#TGT:b6bd33bc-b9b3-489d-badf-67503316e220] and permitted [#SRC:dd33d5b7-2e3a-44fc-b3da-3ec706e631e3].

### Source passage

We may impose a Requirement on a firm under section 35 of FSMR so as to require the firm to take action, or refrain from taking action, specified by us. Section 36 of FSMR sets out further provisions regarding our power to impose Requirements and provides that a Requirement can extend to a firms activities which are not Regulated Activities.

### Target passage

Imposition and variation of requirements. Requirements under section ‎35: further provisions

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `our power to impose Requirements`
- Citation hook: `36`
- Source item type: `Permission`
- Target item type: `Scope`
- Answer spans: 1 span(s) annotated

**LLM-as-judge summary:**
- Fused passed: **False**
- Fused score: **3** (0–10)
- Subscores: correctness=0, dual_use=1, realism=2


---

## QA 8: SCHEMA — eliminated

*persona: **basic** · reference_type: **Internal***

**QA ID:** `cb7f032d-e7e5-4a70-9114-6701027bf46a`

### Question

When an Authorised Person calculates the exposure value for pre-settlement counterparty exposures from SFTs, what steps must they follow if there is no qualifying cross-product netting agreement?

### Expected answer

To calculate the exposure value for pre-settlement counterparty exposures from securities financing transactions (SFTs), an Authorised Person must follow a specific set of steps. First, they need to ensure that the calculation aligns with the International Financial Reporting Standards (IFRS) and the netting requirements outlined in the rules. If there is no qualifying cross-product netting agreement, the calculation must adhere to rules 4.9.15 to 4.9.20. This approach ensures that the exposure value accurately reflects the on-balance sheet value and any potential future exposure. By following these steps, the Authorised Person can ensure that the exposure value is calculated correctly, which is crucial for managing risk and maintaining compliance with regulatory standards [#TGT:5c71feb7-d94a-4998-affb-cb3f15cc55ab] as permitted [#SRC:b0cdb789-c9b6-4f36-a6b3-bf1e213d2007].

### Source passage

In relation to on-balance sheet items: a. for SFTs, the Exposure value should be calculated in accordance with IFRS and the Netting requirements referred to in Rule 4.9.14; b. for Derivatives, including written credit protection, the Exposure value should be calculated as the sum of the on-balance sheet value in accordance with IFRS and an add-on for potential future Exposure calculated in accordance with Rules A4.6.14 to A4.6.21 of App 4; and c. for other on-balance sheet items, the Exposure value should be calculated based on their balance sheet values in accordance with Rule 4.9.3.

### Target passage

Measurement of E for pre settlement Counterparty Exposures arising from SFTs. An Authorised Person must calculate E, for a pre settlement Counterparty Exposure arising from an SFT, other than an Exposure covered by a qualifying cross product Netting agreement, in accordance with Rules 4.9.15 to 4.9.20.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `Exposure value should be calculated`
- Citation hook: `4.9.14`
- Source item type: `Procedure`
- Target item type: `Procedure`
- Answer spans: 1 span(s) annotated

**LLM-as-judge summary:**
- Fused passed: **False**
- Fused score: **5** (0–10)
- Subscores: correctness=2, dual_use=3, realism=2


---

## QA 9: SCHEMA — eliminated

*persona: **professional** · reference_type: **Internal***

**QA ID:** `bbe2aabf-fa5a-4dfe-b56c-cf3a0b2ca05e`

### Question

What documentation must an Authorised Person include in its Resolution Pack concerning individuals critical to operational functions, and how does this relate to those handling Client Money and Safe Custody Assets?

### Expected answer

An Authorised Person is required to include in its Resolution Pack a document that identifies all senior managers, directors, and other individuals who are critical or important to the performance of operational functions related to the obligations imposed on the Authorised Person. This includes individuals within the Authorised Person or elsewhere who are necessary for tasks such as internal and external reconciliations of Client Money, Relevant Money, and Safe Custody Assets, as well as those responsible for client documentation involving these assets. The inclusion of such documentation ensures that the Authorised Person can effectively manage and oversee the operational functions critical to its regulatory obligations, thereby maintaining compliance with the relevant rules. This requirement highlights the importance of clearly identifying and documenting the roles and responsibilities of key individuals involved in handling Client Money and Safe Custody Assets, ensuring that the Authorised Person can swiftly retrieve and manage necessary information in compliance with regulatory standards [#SRC:ad131b2c-da04-4e5f-bbc4-045f5ec9fcf1] and [#TGT:9a2f70fe-ca63-4b72-a573-f428b37a1a24].

### Source passage

For the purpose of Rule 16.3.1(d), examples of individuals within the Authorised Person or elsewhere who are critical or important to the performance of operational function include: (a) those necessary to carry out both internal and external Client Money, Relevant Money and Safe Custody Asset reconciliations; and (b) those in charge of client documentation involving Client Money, Relevant Money and Safe Custody Assets.

### Target passage

An Authorised Person must include within its Resolution Pack: (a) a master document containing information sufficient to retrieve each document in the Authorised Person's Resolution Pack; (b) a document which identifies the institutions the Authorised Person has appointed: (i) in the case of Client Money or Relevant money, to hold and maintain Client Accounts or Payment accounts, respectively; and (ii) in the case of Safe Custody Assets, for the deposit of those assets in accordance with Rule ‎15.5.1; (c) a document which identifies each tied agent, field representative or other agent of the Authorised Person which receives Client Money or Safe Custody Assets in its capacity as the Authorised Person's agent in accordance with Rule ‎15.5.1 and Rule ‎15.6; (d) a document which identifies all senior manager, directors and other individuals, and the nature of their responsibility within the Authorised Person or elsewhere, that are critical or important to the performance of operational functions related to any of the obligations imposed on the Authorised Person by this chapter; (e) for each institution identified in Rule 16.3.1 (b) a copy of each executed agreement, including any side letters or other agreements used to clarify or modify the terms of the executed agreement, between that institution and the Authorised Person that relates to the holding of Client Money, Relevant Money or Safe Custody Assets; (f) a document which: (i) identifies each member of the Authorised Person's Group involved in operational functions related to any obligations imposed on the Authorised Person under this chapter, including, in the case of a member that is a nominee company, identification as such; and (ii) identifies each third party which the Authorised Person uses for the performance of operational functions related to any of the obligations imposed on the Authorised Person by this chapter; (g) for each Group member identified in Rule 16.3.1(b), the type of entity (such as branch, subsidiary and/or nominee company) the Group member is, its jurisdiction of incorporation if applicable, and a description of its related operational functions; (h) a copy of each executed agreement, including any side letters or other agreements used to clarify or modify the terms of the executed agreement, between the Authorised Person and each third party identified in Rule 16.3.1(b); (i) where the Authorised Person relies on a third party identified in Rule 16.3.1(c), a document which describes how to: (i) gain access to relevant information held by that third party; and (ii) effect a transfer of any of the Client Money, Relevant Money or Safe Custody Assets held by the Authorised Person, but controlled by that third party; and (j) a copy of the Authorised Person's manual which records its procedures for the management, recording and transfer of the Client Money, Relevant Money or Safe Custody Assets that it holds.

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `individuals within the Authorised Person`
- Citation hook: `16.3.1(d)`
- Source item type: `Definition`
- Target item type: `Obligation`
- Answer spans: 1 span(s) annotated

**LLM-as-judge summary:**
- Fused passed: **False**
- Fused score: **6** (0–10)
- Subscores: correctness=3, dual_use=4, realism=2


---

## QA 10: SCHEMA — eliminated

*persona: **basic** · reference_type: **Internal***

**QA ID:** `a7e142bd-56c8-4a0b-bf96-2c794d14159f`

### Question

How does an Authorised Person find out which capital instruments can be used for Available Stable Funding, considering the rules for T2 Capital?

### Expected answer

An Authorised Person needs to identify which capital instruments can be used for Available Stable Funding by checking if they meet certain rules. This involves looking at the capital elements that qualify under specific rules, like Rule 3.12.2, and making sure to leave out any Tier 2 capital instruments that have less than one year left until they mature. T2 Capital includes capital instruments that fit the criteria in Rule 3.12.3 and any related Share premium accounts. So, the Authorised Person must ensure that the capital instruments they choose for Available Stable Funding meet these rules and aren't excluded because of their maturity. This careful selection helps keep the financial institution's capital stable and compliant with the necessary regulations [#TGT:2ba8da20-d967-4d1e-bf49-877f5e6ceddb] and [#SRC:28d5816c-6e62-4526-954c-d1c4fa6f17d1].

### Source passage

Available Stable Funding (ASF). Subject to Rule A10.4.6, an Authorised Person must identify its capital instruments that are to be included in its Available Stable Funding by considering the capital elements that are meet the requirements for eligibility under: (a) Rule 3.10.2; (b) Rule 3.11.2; and (c) Rule 3.12.2, excluding all Tier 2 capital instruments with residual maturity of less than one year.

### Target passage

T2 Capital consists of the sum of the following elements: (a) capital instruments which meet the eligibility criteria laid down in Rule 3.12.3; and (b) the Share premium accounts related to the instruments referred to in (a).

**Schema hooks & item types (SCHEMA only):**
- Semantic hook: `identify its capital instruments`
- Citation hook: `3.12.2`
- Source item type: `Obligation`
- Target item type: `Definition`
- Answer spans: 1 span(s) annotated

**LLM-as-judge summary:**
- Fused passed: **False**
- Fused score: **6** (0–10)
- Subscores: correctness=2, dual_use=2, realism=2


---

