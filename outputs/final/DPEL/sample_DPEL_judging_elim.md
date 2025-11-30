# RegRAG-Xref sampled QAs

_Source file: `sample_DPEL_judging_elim.jsonl`_

## QA 1: DPEL — eliminated

*persona: **professional** · reference_type: **Internal***

**QA ID:** `69f890bf-ed3b-4427-bea6-31cabbf09300`

### Question

How must an Authorised Person calculate E* for pre-settlement Counterparty Exposures arising from SFTs when using the FCCA and a qualifying bilateral Netting agreement, and what specific transactions are excluded from this calculation?

### Expected answer

An Authorised Person must calculate E* for all its Credit Risk Exposures to any single Counterparty covered by a qualifying bilateral Netting agreement when using the FCCA, in accordance with Rules A4.3.2 to A4.3.6 in App4, if supervisory or own estimate haircuts are applied [#SRC:56e2cb44-f613-4f2a-bd4c-8726a79a5776]. This calculation specifically excludes collateralised transactions that are not OTC Derivative transactions or long settlement transactions [#TGT:ba7703d2-eb05-4b88-b13a-0dfe34dd09bd].

### Source passage

Measurement of E for pre settlement Counterparty Exposures arising from SFTs. An Authorised Person which has taken eligible financial Collateral for an SFT that is covered by a qualifying bilateral Netting agreement and using the FCCA, must calculate E* for all its CR Exposures to any single Counterparty covered by the qualifying bilateral Netting agreement, in accordance with Rules A4.3.2 to A4.3.6 in App4 (if the Authorised Person is using supervisory haircuts or own estimate haircuts), and substitute E* for E when calculating the Credit Risk weighted Exposure amount for its CR Exposures to that Counterparty under Section 4.8.

### Target passage

Calculation of E* for collateralised transactions other than OTC Derivative transactions and long settlement transactions.

**LLM-as-judge summary:**
- Fused passed: **False**
- Fused score: **5** (0–10)
- Subscores: correctness=2, dual_use=3, realism=2


---

## QA 2: DPEL — eliminated

*persona: **basic** · reference_type: **External***

**QA ID:** `6354f652-4da5-433d-b692-be568a8cb23d`

### Question

How can the regulator suspend a Financial Services Permission, and what does this have to do with disqualifying auditors or actuaries?

### Expected answer

The regulator can suspend a Financial Services Permission for an Authorised Person using powers from FSMR sections 33 and 233 [#SRC:91136058-cc7e-4ef2-a787-46f73fafb584]. This is related to the disqualification of auditors or actuaries because both actions are part of the regulatory authority's ability to enforce compliance and maintain integrity in financial services [#TGT:e7ef987d-e0b0-4f04-bab8-5f4e37805d5c].

### Source passage

The range of powers available to us includes the power to: (a) require information or documents (FSMR sections 201 and 206); (b) require a report from a skilled person (FSMR section 203); (c) impose Requirements on a firm (FSMR section 35); (d) vary, suspend or cancel the Financial Services Permission of an Authorised Person (FSMR sections 33 and 233); (e) impose or vary conditions on an Approved Person on our own initiative (FSMR section 48); (f) give a Direction to a Recognised Body (FSMR section 132); and (g) revoke a Recognition Order (FSMR section 134).

### Target passage

Suspending a Financial Services Permission or Approval or disqualification of auditors or actuaries

**LLM-as-judge summary:**
- Fused passed: **False**
- Fused score: **3** (0–10)
- Subscores: correctness=0, dual_use=1, realism=2


---

## QA 3: DPEL — eliminated

*persona: **basic** · reference_type: **External***

**QA ID:** `19edf5cc-9eaf-4db2-8d92-9e21629bd86c`

### Question

When can certain communications be exempt from the rules about offering securities in the Abu Dhabi Global Market?

### Expected answer

Certain communications can be exempt from the rules about offering securities if the Regulator prescribes them as Exempt Communications under section 59(c) of the FSMR [#SRC:0c1f16b4-30eb-4cf6-845f-2ecc45f1337f]. This means they do not count as an Offer of Securities and are not subject to the prohibition on making such offers in the Abu Dhabi Global Market [#TGT:67094ff0-5048-4e6e-87e4-bb61836c324a].

### Source passage

The Regulator has the power, pursuant to section 59(c) of the FSMR, to prescribe certain communications to be Exempt Communications. Such communications are not subject to the prohibition in section 58(1) of the FSMR as they fall outside the definition of an "Offer of Securities" in section 59 of the FSMR.

### Target passage

A person shall not— (a) make an Offer of Securities in the Abu Dhabi Global Market; or (b) have Securities admitted to trading on a Recognised Investment Exchange; except as provided by or under these Regulations.

**LLM-as-judge summary:**
- Fused passed: **False**
- Fused score: **6** (0–10)
- Subscores: correctness=2, dual_use=2, realism=2


---

## QA 4: DPEL — eliminated

*persona: **basic** · reference_type: **External***

**QA ID:** `2eff5bf5-f872-4d25-9b8c-b620ff2ba95d`

### Question

How can someone be classified as a Professional Client, and what rules define this classification?

### Expected answer

Someone can be classified as a Professional Client by being either a 'deemed' or 'assessed' Professional Client [#TGT:9a802537-4320-4c78-9b40-8bad9941e285]. The rules that define this classification are specified in COBS Rule 2.4.1, which sets out the criteria for being a Professional Client [#SRC:fcb1c541-c9fe-414d-b3a5-f50678fc40a3].

### Source passage

For the purposes of these Rules: (a) the criteria to be classified as a Professional Client are specified in COBS Rule 2.4.1, and (b) the criteria to be classified as a Retail Client are specified in COBS Rule 2.3.

### Target passage

There are two routes through which a Person may be classified as a Professional Client: (a) "deemed" Professional Clients; and (b) "assessed" Professional Clients.

**LLM-as-judge summary:**
- Fused passed: **False**
- Fused score: **6** (0–10)
- Subscores: correctness=3, dual_use=4, realism=2


---

## QA 5: DPEL — eliminated

*persona: **professional** · reference_type: **Internal***

**QA ID:** `fdc57623-e736-4a87-9920-6c3748853115`

### Question

Under what conditions may an Authorised Person apply a 0% risk weight to a CR Exposure involving a guarantee provided by a multilateral development bank (MDB), and which entities are eligible to provide such guarantees?

### Expected answer

An Authorised Person may apply a 0% risk weight to a CR Exposure if the exposure is to specific multilateral development banks such as the Bank for International Settlements, the International Monetary Fund, the European Central Bank, or the European Commission [#TGT:eee311ad-dd67-489b-99c2-e2d73f7efc16]. Additionally, for the effects of credit risk mitigation (CRM) of a guarantee to be recognised, the guarantee must be provided by entities including central governments, central banks, certain MDBs as referred to in Rule 4.12.8, international organisations as per Rule 4.12.9, public sector enterprises (PSEs), banks and securities firms qualifying for the bank asset class, or any entity with a credit assessment mapping to Credit Quality Grade 3 or better [#SRC:281505d3-a15a-449a-9095-dc247d0e2e5d].

### Source passage

An Authorised Person may recognise the effects of CRM of a guarantee only if it is provided by any of the following entities: (a) central government or central bank; (b) MDB referred to in Rule 4.12.8; (c) International Organisations referred to in Rule 4.12.9; (d) PSE; (e) banks and Securities firms which qualify for inclusion in bank asset class; or (f) any other entity that has an external credit assessment from a recognised credit rating agency that maps to a Credit Quality Grade 3 or better.

### Target passage

Multilateral development bank (MDB) asset class. An Authorised Person must apply a 0% risk weight to any CR Exposure to the Bank for International Settlements, the International Monetary Fund, the European Central Bank or the European Commission.

**LLM-as-judge summary:**
- Fused passed: **False**
- Fused score: **6** (0–10)
- Subscores: correctness=2, dual_use=2, realism=2


---

## QA 6: DPEL — eliminated

*persona: **professional** · reference_type: **Internal***

**QA ID:** `c4ca3877-6da1-49ea-9816-6c80891ddcee`

### Question

How should an Authorised Person risk weight a CR Exposure in the central government and central bank asset class if the requirements of Rule 4.12.5 are not met?

### Expected answer

If the requirements of Rule 4.12.5 are not met, the CR Exposure should be treated in accordance with Rule 4.12.4 [#SRC:d005dde9-921a-4f5c-ac96-c708712bf938]. For CR Exposures in the central government and central bank asset class, an Authorised Person must apply the risk weights specified in the table, subject to Rules 4.12.5 [#TGT:f3576eb9-2d51-4fbe-bf30-26823907def6].

### Source passage

Where the requirements of Rule 4.12.5 are not met the CR Exposure should be treated in accordance with Rule 4.12.4.

### Target passage

Central government and central bank asset class. Subject to Rules 4.12.5, an Authorised Person must risk weight any CR Exposure in the central government and central bank asset class in accordance with the table below. Risk weights for the central government and central bank asset class /Table Start Credit Quality Grade 1 2 3 4 5 6 Unrated Risk Weight 0% 20% 50% 100% 100% 150% 100% /Table End

**LLM-as-judge summary:**
- Fused passed: **False**
- Fused score: **6** (0–10)
- Subscores: correctness=2, dual_use=3, realism=2


---

## QA 7: DPEL — eliminated

*persona: **professional** · reference_type: **External***

**QA ID:** `e2659a62-5a80-44d5-9452-a04814849bd3`

### Question

Under what circumstances may the Regulator vary or cancel the Financial Services Permission of an Authorised Person, and how does this relate to the powers outlined in FSMR sections 33 and 233?

### Expected answer

The Regulator has the authority to vary or cancel the Financial Services Permission of an Authorised Person on its own initiative, as outlined in the TARGET passage [#TGT:445d41e7-27aa-41c1-84e4-194553261f8a]. This action is supported by the powers granted under FSMR sections 33 and 233, which are specifically mentioned in the SOURCE passage as part of the Regulator's range of powers [#SRC:91136058-cc7e-4ef2-a787-46f73fafb584]. The ability to vary or cancel permissions is a critical tool for the Regulator to ensure compliance and maintain the integrity of the financial system. The process involves assessing whether the conditions for holding such permissions are still being met by the Authorised Person, and if not, the Regulator may take action to vary or cancel the permissions as necessary.

### Source passage

The range of powers available to us includes the power to: (a) require information or documents (FSMR sections 201 and 206); (b) require a report from a skilled person (FSMR section 203); (c) impose Requirements on a firm (FSMR section 35); (d) vary, suspend or cancel the Financial Services Permission of an Authorised Person (FSMR sections 33 and 233); (e) impose or vary conditions on an Approved Person on our own initiative (FSMR section 48); (f) give a Direction to a Recognised Body (FSMR section 132); and (g) revoke a Recognition Order (FSMR section 134).

### Target passage

Variation and cancellation of a Financial Services Permission. Variation or cancellation on initiative of the Regulator

**LLM-as-judge summary:**
- Fused passed: **False**
- Fused score: **5** (0–10)
- Subscores: correctness=0, dual_use=3, realism=2


---

## QA 8: DPEL — eliminated

*persona: **professional** · reference_type: **External***

**QA ID:** `48679c3b-5d2d-4cb1-86b3-d51b92d65851`

### Question

How must an Issuer ensure compliance with the requirements for Offers of Securities under FSMR when making statements about future matters to the public in ADGM?

### Expected answer

An Issuer making an Offer of Securities to the Public in or from ADGM must comply with the requirements set out in Sections 58 to 71 of FSMR and Chapter 4 of the Markets Rules (MKT), which include the obligation to publish a Prospectus under Section 61 of FSMR [#SRC:d7598df9-aeea-4b2d-b1ef-e4e98bea49dd]. When making statements about future matters, the Issuer must ensure that these statements are not misleading or deceptive, as such conduct could contravene the regulatory framework governing securities offers [#TGT:c7e8bce4-0757-4052-b618-aedbbe7000a8].

### Source passage

Regulatory treatment of tokens deemed to be Securities. The requirements for Offers of Securities fall under Sections 58 to 71 of FSMR and Chapter 4 of the Markets Rules (MKT). When an Issuer wishes to make an Offer of Securities to the Public in or from ADGM, these requirements include, for example, the obligation to publish a Prospectus under Section 61 of FSMR.

### Target passage

Misleading and deceptive statements or omissions. Statements about future matters

**LLM-as-judge summary:**
- Fused passed: **False**
- Fused score: **6** (0–10)
- Subscores: correctness=2, dual_use=2, realism=2


---

## QA 9: DPEL — eliminated

*persona: **professional** · reference_type: **Internal***

**QA ID:** `8269ace3-e065-4593-9c42-175026d9dc9f`

### Question

How frequently must an Authorised Person in Category 1, 2, 3A, or 5 calculate its NSFR to ensure compliance with Rule 10.4.1, and under what conditions should this calculation be adjusted?

### Expected answer

An Authorised Person in Category 1, 2, 3A, or 5 must calculate its Net Stable Funding Ratio (NSFR) with sufficient frequency to ensure continuous compliance with Rule 10.4.1 [#TGT:c6a601d3-a2ca-464f-820c-bdd74b7e1759]. Additionally, the calculation should be adjusted whenever there is a belief that a change has occurred in its Available Stable Funding or Required Stable Funding that could materially affect the NSFR level [#SRC:50aee557-426a-475b-bbf3-73ca3ea00933].

### Source passage

An Authorised Person should calculate its NSFR with appropriate frequency to ensure that it is able to monitor its satisfaction of the requirement in Rule 10.4.1 at all times and, additionally, where it believes that a change has happened to its Available Stable Funding or Required Stable Funding that might result in a material change to the level of its NSFR.

### Target passage

This Section applies to an Authorised Person in Category 1, 2, 3A or 5.

**LLM-as-judge summary:**
- Fused passed: **False**
- Fused score: **6** (0–10)
- Subscores: correctness=2, dual_use=3, realism=2


---

## QA 10: DPEL — eliminated

*persona: **professional** · reference_type: **External***

**QA ID:** `5b8f2c11-92f6-41fe-b51b-a6c57dbb4a46`

### Question

Under what circumstances may the FSRA cancel a Financial Services Permission on its own initiative, and how does this relate to the Regulator's objectives?

### Expected answer

The FSRA may cancel a Financial Services Permission on its own initiative if it appears that the FinTech Participant is failing, or is likely to fail, to satisfy the Threshold Conditions as outlined in section 7(2) of the FSMR [#SRC:a196fe29-bdce-4820-ad63-7fbde525c991]. This action may also be taken if it is deemed desirable to further one or more of the Regulator's objectives, such as when the FinTech Participant is not meeting the authorisation requirements or the limitations and conditions specified in the Guidance [#SRC:a196fe29-bdce-4820-ad63-7fbde525c991]. The cancellation process is part of the broader regulatory framework that includes both variation and cancellation of Financial Services Permissions on the Regulator's initiative [#TGT:445d41e7-27aa-41c1-84e4-194553261f8a].

### Source passage

Cancellation of the FSP. FSRA may cancel the FSP on the application of the FinTech Participant, in accordance with section 32 of the FSMR, or on the initiative of the Regulator, in accordance with section 33 of the FSMR, if it appears to the Regulator that: (a) the FinTech Participant is failing, or is likely to fail, to satisfy the Threshold Conditions made under section 7(2) of the FSMR and set out in paragraph 5.2(a) of this Guidance; (b) it is desirable to exercise this power to further one or more of the Regulators objectives, including, for example, if: i. the FinTech Participant is failing, or is likely to fail, to satisfy the authorisation requirements set out in section 5.2(b) (f) of this Guidance; or ii. the FinTech Participant is failing, or is likely to fail, to satisfy the limitations or conditions set out in section 7.1 of this Guidance; or (c) the FinTech Participant has committed a contravention of the FSMR or any Rules made under the FSMR.

### Target passage

Variation and cancellation of a Financial Services Permission. Variation or cancellation on initiative of the Regulator

**LLM-as-judge summary:**
- Fused passed: **False**
- Fused score: **5** (0–10)
- Subscores: correctness=2, dual_use=2, realism=2


---

