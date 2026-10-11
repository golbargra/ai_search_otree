<div role="main">

# AI product-search experiment

**Research proposal and session protocol**  
Classroom study • Four groups • One session • Live product search

We want to understand whether AI helps people find products faster, whether their choices meet the requirements, and what changes when they can use AI and search together. Participants will complete short shopping tasks using an assigned set of tools. We will compare their time, accuracy, search behavior, and experience.

The study will use a balanced, between-subjects design with three groups: Google Web search, ChatGPT, and ChatGPT plus Google Web search. Each participant will complete three product-search tasks in one classroom session. oTree will manage assignment, task delivery, timing, and submissions. Product information will be verified against live-web evidence captured during the tasks.

Product search is a useful setting because the task requirements can be stated clearly while the search process remains open. A participant may receive a confident recommendation quickly but still choose a product that fails a requirement. Another participant may take longer because they check the details. Measuring time and verified accuracy separately will help distinguish these outcomes. Search records and participant ratings will provide additional evidence about verification, effort, and confidence.

## 1. Study objective and research questions

The main objective is to estimate how access to different search tools affects performance on a task with clear requirements. Random assignment lets us compare the effect of the assigned tools. It does not separately identify the causal effect of choosing to use AI within the combined group.

<table>
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<thead>
<tr class="header">
<th>Area</th>
<th>Questions</th>
<th>Main measures</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>Productivity</td>
<td>RQ1. Does AI change how quickly people finish?<br />
RQ2. Does AI change how often they find a product meeting every requirement?<br />
RQ3. Does having both AI and search improve correct completions per minute?<br />
RQ4. How does default Google compare with Google’s Web filter?</td>
<td>Task time, verified success, share of requirements met, correct completions per minute</td>
</tr>
<tr class="even">
<td>How the effect occurs</td>
<td>RQ5. Do the groups differ in verification, search effort, or types of errors?<br />
RQ6. Do differences in confidence and mental effort match actual performance?</td>
<td>Queries, messages, product visits, verification actions, error codes, confidence and effort</td>
</tr>
<tr class="odd">
<td>Who benefits</td>
<td>RQ7. Do people with less prior AI experience benefit more?<br />
RQ8. Do shopping experience and product familiarity relate to these differences?</td>
<td>Condition × prior experience; shopping frequency; category familiarity</td>
</tr>
<tr class="even">
<td>Product choices</td>
<td>RQ9. Do the groups choose different prices, ratings, products, or retailers?<br />
RQ10. Do choices appear more concentrated in AI groups, given that tasks differ?</td>
<td>Selected price and rating; descriptive product and retailer shares</td>
</tr>
</tbody>
</table>

The last question will be exploratory. Individualized tasks give participants different requirements and possibly different feasible products. We cannot make a clean claim about people choosing the same product for the same task without shared tasks.

## 2. Experimental groups

Each participant will be assigned to one group using a fixed S/A/B cycle and remain in that group for the full session. This avoids carrying experience from one experimental tool condition into another. Participants can still learn across tasks within their assigned group.

| Group             | Tools available                                                                                  | What the comparison tells us                                                |
|-------------------|--------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| S: Search only    | Google using the Web filter; product pages reached from those results                            | Reference condition without Google AI Overviews or a separate AI assistant  |
| A: AI only        | A study AI assistant with live web access; direct source/product links returned by the assistant | AI as the route for finding products, with linked-page verification allowed |
| B: AI and search  | The same assistant as A, plus the same Web-filter Google access as S                             | Effect of making AI available alongside conventional search                 |

“AI only” means participants cannot independently search Google or retailer search boxes. They may open direct product links supplied by the assistant to inspect the offer. In all groups, selecting a variant or checking information on a linked product page is allowed. Starting a separate retailer search or browsing unrelated categories is not allowed. This keeps product discovery tied to the assigned tools.

Participants in B may choose either tool or both and remain in B for analysis. The Web-filter launch route (`udm=14`) must be checked immediately before class. S and B must avoid Google AI Mode and other AI tools.

### Assignment and technical consistency

Participants are allocated when the session is created, cycling S, A, B by participant slot. `ai_search` requires a multiple of three: 69 gives 23 per arm; 72 gives 24 per arm. `ai_search_70` explicitly permits 24/23/23 so all 70 students can participate. Seventy cannot be split exactly equally across three arms. These are assigned-slot counts; withdrawals, unused links, and comprehension exclusions can reduce completed counts unevenly. Do not remove completed observations just to equalize groups.

Assignment is stored in every round and revealed after baseline items. There is no mutable allocation queue during concurrent survey submissions. Prior AI use is measured but no longer defines assignment strata. The fixed cycle meets the requested nonrandom allocation, but arrival-ordered links can associate condition with arrival time. Distribute participant links without using performance or prior experience to select conditions, record how they were distributed, and avoid describing the fixed cycle as randomization.

Every consecutive triplet receives the same seeded task battery and order, with one slot per arm. Batteries vary across triplets. This matches task composition across arms when all slots participate.

The implemented version opens the public ChatGPT website in an external tab. It has no embedded assistant or shared AI API quota. A and B should use the same model and web-access settings where available, and start a fresh chat for each task. Check account access and limits before class. oTree logs launcher events, not external conversations or complete browsing histories. Screen recording requires a separately arranged workflow; the app does not implement recording.

## 3. Hypotheses

H1–H3 will be the primary hypotheses. H4–H8 will be secondary, with H7 limited to descriptive exploration under this design. The explanations below are proposed mechanisms. Observing the predicted outcome does not by itself prove the mechanism.

| Hypothesis               | Prediction and reasoning                                                                                                                                                                                  | Measure and comparison                                                                                                                                        |
|--------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| H1: Speed                | A will be faster than B, and B faster than S. AI may reduce the time spent looking through results; using both tools may add verification time.                                                           | Elapsed task time: A \< B \< S. Test A–B and B–S; report timeouts and accuracy alongside time.                                                                |
| H2: Accuracy             | B will produce more fully correct choices than S and A because participants can check AI suggestions against product information.                                                                         | Verified success: B \> S and B \> A. Share of requirements met is a supporting outcome.                                                                       |
| H3: Overall productivity | B will produce more correct completions per minute than S and A. Access to both tools may combine quick discovery with checking.                                                                      | Participant-level verified correct tasks divided by total task minutes: B–S, B–A.                                                                        |
| H4: Speed and errors     | A will be faster but less accurate than S. Compared with S, A will show more submitted factual claims contradicted by product-page evidence; S will show more missing or unchecked requirements.          | A–S success contrast, H1 timing evidence, and separately coded error and verification measures. Error origin is coded only when supported by records.         |
| H5: Prior experience     | The performance benefit of A or B relative to S will be larger among participants with less prior AI use.                                                                                                 | Condition × baseline AI-use frequency. Benefits mean higher accuracy/productivity or lower time; interpret the sign separately for each outcome.              |
| H6: Product choice       | A and B will select lower-priced products than S, after accounting for assigned category and price range.                                                                                                 | Verified selected price and position within the assigned price band. Report whether choices meet all requirements. Lower price alone is not “better quality.” |
| H7: Concentration        | AI groups may choose from fewer retailers or products.                                                                                                                                                    | Exploratory retailer/product shares and HHI within category/difficulty groups. Different feasible sets prevent a clean identical-task concentration test.     |
| H8: Perceptions          | A and B will report more ease and reuse intention than S; S will report more trust. Perceived advertising influence will be tested for equivalence rather than inferred from a nonsignificant difference. | Post-study ratings; planned A–S and B–S comparisons. TOST for perceived advertising influence using prespecified bounds.                                      |

H4 tests a directional S–A difference; lack of significance does not establish equality.

For H8, a proposed equivalence range is −0.5 to +0.5 points on the 1–7 advertising-influence item. The team must justify and lock this range before collecting outcome data. Equivalence requires the full 90% confidence interval to lie within the range for the relevant TOST comparison; otherwise the finding can be inconclusive.

## 4. Participants and sample size

We will recruit about 70 students from one class. Each completes three scored tasks. With 69 participants there are up to 207 scored attempts, with 23 people per arm; with all 70 there are up to 210 attempts, with 24/23/23 assigned slots.

These repeated tasks give us more information about each student's performance, but they do not replace having more participants. We will treat this classroom study as a pilot, focusing on differences in time and accuracy. Comparisons based on prior AI experience will be exploratory because each group will be small.

Participation will be voluntary and will not affect course grades. If course credit is offered, an equivalent alternative will be available. We will collect data in one classroom session, after a small usability check of the tasks and software.

## 5. Tasks and task bank

Each participant will complete one practice task and three scored tasks. This is the proposed starting load for a 30–35 minute classroom session. Each scored task has a four-minute limit and asks the participant to find one product meeting all listed requirements. More than one answer may be correct.

Each participant receives one easy, one medium, and one hard task, selected from the six-category finite bank. Consecutive S/A/B triplets share categories, variants, and task order. Across triplets, seeds select categories and variants and shuffle order; task instances are not guaranteed unique.

| Template            | Illustrative requirements                                                                                   | Planned difficulty |
|---------------------|-------------------------------------------------------------------------------------------------------------|--------------------|
| Wireless mouse      | \$15–\$35; at least 4.0 stars; at least 100 customer ratings; in stock                                      | Easy               |
| Electric kettle     | \$25–\$55; at least 4.0 stars; at least 200 customer ratings; in stock                                      | Easy               |
| Wireless headphones | \$40–\$80; at least 4.2 stars; at least 200 customer ratings; in stock; built-in microphone                 | Medium             |
| Laptop backpack     | \$30–\$60; at least 4.2 stars; at least 150 customer ratings; in stock; fits a 15.6-inch laptop             | Medium             |
| Cordless vacuum     | \$70–\$120; at least 4.3 stars; at least 300 customer ratings; in stock; stated weight under 6 lb           | Hard               |
| Portable speaker    | \$35–\$65; at least 4.3 stars; at least 300 customer ratings; in stock; stated IPX7 water-resistance rating | Hard               |

The examples below define the intended task format. Their current feasibility will be checked before use. Before launch, the team will check each allowed parameter combination and retain only combinations with several feasible offers. Use a finite, prechecked parameter bank rather than unrestricted random numbers. Assign task instances independently of tool condition and randomize task order. Save the exact requirements and the randomization seed.

Each person receives one easy, one medium, and one hard task. Difficulty will be based on pilot completion and feasibility, not only the number of requirements. Recheck feasibility shortly before the session. These checks establish task feasibility. Participants can submit any qualifying live offer, including products not found during preparation.

### Exact task instructions

> Find one new product that meets every requirement shown below. Use only your assigned tools. You may inspect permitted product links to check the details. Enter the product name, retailer, price, rating, number of customer ratings, availability, and product-page link. You have four minutes. You do not need to buy anything. More than one answer can be correct. If you cannot find a suitable product, select “I could not find one.”

The goal is to find a qualifying product, not necessarily the cheapest or highest-rated product. We therefore will not call a price difference an optimality gap. The global cheapest feasible product is not observable reliably in an unrestricted live-web search.

### Common scoring definitions

- Use new products sold in US dollars. Exclude used, refurbished, auction, subscription-only, and membership-only offers.
- Price is the displayed one-time item price for the chosen variant, before shipping and tax. Do not count optional coupons or discounts requiring a separate action. Save shipping information if shown, but do not score it unless the task explicitly requires it.
- Use a rating on a five-star scale and the number of customer ratings attached to that rating. Do not mix this with the number of written reviews. If the site only reports a rounded count that cannot establish the threshold, code the requirement as unverifiable.
- In stock means the selected variant can be ordered and is not marked unavailable, preorder, or backorder. Do not require delivery within a specified number of days in this version.
- Use the retailer page’s displayed product-level rating, noting whether it combines variants. Evaluate price, stock, and technical attributes for the selected variant.
- Use the same location setting when a retailer requests one. Record it in session metadata before launch.

## 6. Answer form and live-web verification

oTree will record what the participant submits. The research team will then verify the answer using the product page and evidence recorded during the task. Participant-entered numbers are reported claims, not verified ground truth.

| Answer field            | Entry                                                                                    |
|-------------------------|------------------------------------------------------------------------------------------|
| Product identity        | Brand, product/model name, selected size/color/variant where relevant                    |
| Offer identity          | Retailer, marketplace seller if applicable, direct product URL                           |
| Product facts           | Price in USD, star rating, customer-rating count, stock status, optional attribute value |
| Unavailable information | “Could not verify” option for each fact; do not force invented values                    |
| Task result             | Submit selected product / I could not find one                                           |

The proposed collection setup records the study browser during scored tasks, with explicit consent. It excludes audio and webcam recording. Use clean study browser profiles and ask participants to close personal content. A participant-initiated capture of the final product page should preserve visible price, rating, count, stock, and variant information where available. A screenshot of an AI answer records what the assistant said; it does not prove those facts.

Reviewers will verify submissions as soon as possible after the session. They will prioritize contemporaneous retailer-page evidence from the task, then an immediate follow-up retailer check. Record both the submission time and the verification time. If a later page differs and no task-time evidence resolves the conflict, mark the affected fact as unverifiable. The scoring decision will reflect the evidence available for the participant’s task time.

Each requirement receives one of three codes: met, not met, or unverifiable. A fully verified correct answer has every requirement marked met. An answer with any known failure is incorrect. An answer with no known failure but an unresolved requirement remains uncertain about true correctness.

The primary outcome is **verified success**: 1 only when all requirements are confirmed; 0 otherwise, including no answer. Preserve a separate uncertainty flag so “not verified correct” is not reported as “proven wrong.” Report uncertainty rates by group and success bounds treating uncertain submitted answers first as failures and then as successes. This matters if AI-only choices provide less verifiable evidence.

A second reviewer will independently score a random 20% of submissions and all ambiguous cases. Score accuracy from an answer/evidence packet with condition hidden where feasible. Review tool transcripts separately for mechanism coding. Resolve disagreements and retain both initial and final codes.

## 7. Variables and measures

### Assignment, task, and outcome data

| Variable                                           | Definition                                                                                              | Source                                                  |
|----------------------------------------------------|---------------------------------------------------------------------------------------------------------|---------------------------------------------------------|
| `participant_id, arm, randomization_block`         | Anonymous code; assigned S/A/B; matched allocation triplet                                                      | oTree                                                   |
| `task_id, template_id, task_order, difficulty`     | Individual instance, underlying category template, position, preassigned difficulty                     | oTree                                                   |
| `task_params`                                      | Exact category, price bounds, thresholds, and attribute requirement                                     | oTree                                                   |
| `start_ts, end_ts, time_sec`                       | Task reveal to final answer, explicit no-answer submission, or deadline; survey time excluded           | oTree server timestamps                                 |
| `submitted, no_answer, timed_out`                  | Separate completion-status indicators; an unsubmitted draft is not a final answer                       | oTree                                                   |
| `verified_success`                                 | 1 if every requirement is verified met; 0 otherwise                                                     | Reviewer scoring imported into data                     |
| `constraint_status_*`                              | Met / not met / unverifiable for each requirement                                                       | Reviewer scoring                                        |
| `n_met, n_failed, n_unknown, k`                    | Requirement counts and total number of requirements                                                     | Derived from scoring                                    |
| `prop_met`                                         | Number verified met divided by k; unknowns are not counted as met                                       | Derived; report uncertainty alongside it                |
| `correct_per_min`                                  | For each participant: total verified correct tasks ÷ total elapsed task minutes across all three attempts | Derived after verification                              |
| `reported_*` and `verified_*`                      | Separate submitted and checked price, rating, count, stock, and attribute fields                        | Answer form and reviewer                                |
| `product_key, offer_key, retailer_key`             | Standardized model/variant, retailer/seller offer, and retailer identity; raw URL retained              | Post-session coding                                     |
| `price_band_position`                              | (Verified price − task minimum) ÷ (task maximum − task minimum); do not clip values outside 0–1         | Derived; compare within category and report feasibility |
| `evidence_id, verified_at, reviewer_id, uncertain` | Evidence location, verification time, scorer, and unresolved status                                     | Review record                                           |

The price measure will be the selected offer’s listed price because participants will not make a purchase. Global price gaps, rating gaps, and composite optimality scores will not be calculated: the study does not observe every feasible live offer, and the task does not specify how price should trade off against rating.

### Process and error measures

| Variable                            | Definition and collection limit                                                                                                                                               |
|-------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `n_queries, query_text`             | Submitted Google searches. Record launcher searches automatically; code subsequent external searches from recordings. Incomplete footage means missing, not zero.             |
| `n_ai_turns, ai_transcript`         | Participant messages and assistant replies; automatic if the assistant is integrated                                                                                          |
| `n_products_viewed`                 | Distinct product pages visibly opened, not products merely mentioned in results; recording-based outside oTree                                                                |
| `first_action_sec`                  | Time to first search/message; identify whether obtained from an app event or recording                                                                                        |
| `n_revisions`                       | Changes to the selected product/URL after the first complete candidate, not individual keystrokes                                                                             |
| `used_search, used_ai`              | At least one actual search/message; pane opening alone does not count                                                                                                         |
| `verification_actions`              | Observable opening/inspection of evidence for a requirement. Viewing a page does not prove the participant read or understood it.                                             |
| `ai_wait_sec, technical_error`      | External AI wait/failure measures require recording review; the app has no API timing log. Waiting remains part of task time.                                                                             |
| `focus_lost`                        | Leaving the oTree tab. Expected during permitted external searches; never an automatic cheating or exclusion measure.                                                         |
| `missing_claim, contradicted_claim` | Required fact omitted; submitted fact contradicted by evidence. These may coexist on different requirements.                                                                  |
| `ai_error_carried_forward`          | Assistant gave a contradicted fact and the participant used it in the submitted answer; requires transcript plus product evidence                                             |
| `error_source`                      | Supported source: assistant, search snippet, product-page misunderstanding, transcription, or unknown. Do not infer cause from assigned group.                                |
| `sponsored_exposure`                | Visible sponsored label on the result through which a selected product was reached, when observable. Advertising is a placement attribute, not a permanent product attribute. |

### Choice concentration

For descriptive exploration, calculate product and retailer shares within category and broad difficulty groups. HHI is the sum of squared choice shares. Pairwise overlap is the fraction of distinct participant pairs selecting the same coded product within a comparable category. Do not compare a participant’s different tasks as if they were independent shoppers facing the same choice.

Report subgroup sample sizes and parameter distributions. Small cells and different requirements make these measures unstable and potentially misleading. We will not use H7 to claim AI causes identical-task convergence or changes market concentration. If there are too few comparable observations, report counts and shares without an HHI test.

## 8. Exact survey questions

### Before assignment

| Measure                 | Question                                                                                  | Responses                                                                                                       |
|-------------------------|-------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| Demographics            | What is your age group? What is your year of study? What is your major?                   | 18–20 / 21–24 / 25–29 / 30+ / prefer not to say; first / second / third / fourth / graduate / other; major text |
| PS1: Familiarity        | How familiar are you with AI chat tools such as ChatGPT, Gemini, or Claude?               | 1 not at all; 2 slightly; 3 moderately; 4 very; 5 extremely                                                     |
| PS2: Use frequency      | During the past month, how often did you use an AI chat tool?                             | 1 never; 2 less than weekly; 3 one or two days a week; 4 three to five days a week; 5 six or seven days a week  |
| PS3: AI shopping use    | During the past month, how often did you use AI to find or compare products?              | Same frequency categories as PS2                                                                                |
| PS4: Self-rated ability | How would you rate your ability to get useful results from AI chat tools?                 | 1 very low to 5 very high                                                                                       |
| Search experience       | During the past month, how often did you use a search engine to find or compare products? | Same frequency categories as PS2                                                                                |
| Shopping frequency      | During the past three months, how often did you buy something online?                     | Never / less than monthly / one to three times a month / about weekly / several times a week                    |
| Category familiarity    | How familiar are you with shopping for each of these products?                            | 1 not at all to 5 extremely; one item per task category                                                         |
| Attention check         | For this item, please select “Sometimes.”                                                 | Never / rarely / sometimes / often / very often                                                                 |

PS2 will be the primary prior-experience moderator. PS1, PS3, and PS4 will remain separate supporting measures because familiarity, frequency, and self-rated ability represent different aspects of experience.

The baseline knowledge measure will contain three questions, each with a “Not sure” option: (1) “AI chat tools can state incorrect facts confidently.” True/False/Not sure; correct: True. (2) “Which source is generally best for checking a product’s current listed price?” Retailer product page / AI answer without a source / social-media post / Not sure; correct: retailer page. (3) “A product review or rating count given by an AI chat tool is always current.” True/False/Not sure; correct: False. Score 0–3, counting Not sure as incorrect. Call this `ai_limitations_knowledge`, not a validated broad AI-literacy scale. Do not provide feedback before tasks; the questions may still prime verification, a limitation shared across groups.

### Comprehension check

1.  Must the selected product meet all requirements or only some? **All.**
2.  Can you use tools other than those assigned? **No.**
3.  Must you buy the product? **No.**
4.  What should you do if you cannot find a product? **Choose “I could not find one.”**
5.  In your assigned group, which tools and product links are permitted? **Show group-specific options and score against Section 2.**

Explain incorrect answers and allow a retry. If someone still cannot follow the instructions after two attempts, provide one standardized clarification. If they still do not understand, do not start their scored tasks; record this outcome by assigned group.

### After each task

1.  “How confident are you that your selected product meets every requirement?” 1 not at all confident to 7 completely confident. Show only if a product was submitted.
2.  “How difficult was this task?” 1 very easy to 7 very hard.
3.  “How much mental effort did this task require?” 1 very little to 7 very much.

These are short self-report items. Difficulty is a possible treatment outcome, so it will not be used as a baseline control in the main model. Confidence is ordinal; do not interpret a 6/7 response as a probability of correctness.

### After all tasks

Introduce the block with: “Think about the tool or combination of tools assigned to you.” Use 1 strongly disagree to 7 strongly agree, with a separate “Cannot judge” option.

1.  The assigned tools made it easy to find a product meeting the requirements.
2.  I trusted the product information provided by the assigned tools.
3.  I would use these tools again for this type of product search.
4.  The results seemed influenced by advertising or paid placement.
5.  The assigned tools helped me finish quickly.

Ask overall mental demand, effort, and frustration separately on 1–7 scales, from very low to very high. These are adapted workload items, not a full NASA-TLX score. End with: “What made the tasks easy or difficult?” and “Was anything confusing or missing?”

For B only, add: “Did you mainly use search, mainly use AI, or use both about equally?” This is a perception check; observed behavior remains the preferred tool-use measure.

## 9. Session flow

| Stage                          | What happens                                                                                | Time                  |
|--------------------------------|---------------------------------------------------------------------------------------------|-----------------------|
| Consent and setup              | Explain tasks, recording, voluntary participation, and anonymous codes; check study browser | 3 minutes             |
| Pre-survey                     | Background, knowledge, attention check; reveal preassigned arm after baseline items                      | 4 minutes             |
| Instructions and comprehension | Show assigned tools and answer rules; comprehension check                                   | 3 minutes             |
| Practice                       | One unscored task using assigned tools; demonstrate answer and evidence submission          | 3 minutes             |
| Scored tasks                   | Three tasks, up to four minutes each; order randomized; no correctness feedback               | Up to 12 minutes      |
| Task ratings                   | Brief ratings after each attempt                                                            | About 2 minutes total |
| Post-survey and debrief        | Perceptions, workload, feedback; explain later scoring and payment                          | 4 minutes             |

Allow about 30–35 minutes, with a small buffer for setup. The timer starts when requirements are revealed. It continues during external browsing and AI waiting. The same deadline persists after refreshing or returning to oTree. The answer form autosaves a draft, but a final answer must be confirmed before the deadline. If time expires, mark a timeout and keep the draft for audit without treating it as a submitted answer.

Practice may include feedback about the interface and rules. Scored tasks will not show accuracy feedback, because that could change later verification behavior.

A proposed payment is \$5 participation plus \$0.50 per verified correct task, up to \$6.50 total. These are planning amounts, subject to the team’s budget and approved consent procedure. Fix and disclose them before recruitment. Base payment is not conditional on accuracy. Pay any performance bonus after verification; do not promise immediate automatic earnings. The end screen confirms completion and explains the payment schedule stated in consent.

## 10. What needs to be built in oTree

oTree manages consent, surveys, fixed assignment, task parameters, deadlines, submissions, and exports. The implementation uses external Google and ChatGPT tabs. It does not contain an AI API pane, browser recording, or automatic correctness verification.

| Component | Implemented behavior |
|---|---|
| Page sequence | Consent → Background → Knowledge → Instructions → Comprehension (up to 3 attempts) → Practice → 3 scored Task/Rating rounds → Post-survey → Completion |
| Assignment | S/A/B cycle at session creation; equal mode requires a multiple of 3; explicit near-equal mode accepts 70 |
| Task bank | One easy, medium, hard per person; same battery and order within each allocation triplet |
| Tools | Web-filter Google for S/B; public ChatGPT tab for A/B |
| Logging | Launcher queries, AI opens, focus changes, draft, final answer and timing; no external chat capture |
| Timing | Persistent server deadline and draft recovery; late/timeout submissions flagged |
| Scoring | Reviewers verify product claims later; no automatic correctness bonus calculation |
| Evidence | Separate recording/capture process must be arranged before retaining the consent recording claim |

For concurrent classroom operation and tests, see the README. Browser restrictions mean oTree cannot read activity inside Google, ChatGPT, or retailer tabs. External process measures require separately collected evidence and must be marked missing when unavailable.

## 11. Analysis plan

Analyze participants according to their assigned group. The main comparisons concern tool availability. Comparisons of actual AI users versus nonusers inside B are descriptive because people choose whether to use it.

| Outcome                | Planned analysis                                                                                                                                                                                                                                                                                               |
|------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Verified success, H2   | Logistic mixed model with condition, template/category, preassigned difficulty, task order, and baseline AI-use frequency; participant random intercept. Report predicted probabilities and percentage-point differences.                                                                                          |
| Time, H1               | Analyze all-attempt elapsed time, including early no-answer exits and deadline-valued timeouts, with participant dependence accounted for. Report timeout and no-answer rates separately. A secondary time-to-submission model can treat timeouts as censored. Faster exit alone is not successful completion. |
| Productivity, H3       | Participant-level correct tasks per total task minute, including failed/no-answer attempts and full deadlines for timeouts. Compare groups with allocation-triplet-adjusted inference or participant-level regression; assess distribution in pilot.                                                              |
| Partial accuracy       | Compare verified-met proportion while retaining k and uncertain counts; repeated attempts remain clustered within participants.                                                                                                                                                                                |
| Errors and process, H4 | Compare recorded error rates and verification behaviors. Distinguish observed actions from inferred mechanisms; use participant-level resampling or suitable count/binary models.                                                                                                                              |
| Prior experience, H5   | Add condition × PS2 to success, time, and productivity models. Treat ordinal PS2 trend as a prespecified simplification and show descriptive category patterns. Interactions are likely imprecise in a small class.                                                                                            |
| Price and rating, H6   | Compare within category, adjusting for assigned bounds and thresholds. Feasible-choice-only comparisons are secondary and selected by a treatment-affected outcome, so they are not unconditional causal effects.                                                                                              |
| Concentration, H7      | Descriptive category-level counts, shares, overlap, and HHI where cell sizes permit; no confirmatory same-task claim                                                                                                                                                                                           |
| Perceptions, H8        | Between-group comparisons, not paired AI-versus-search tests; ordinal models or prespecified mean comparisons. TOST for the advertising-influence item with bounds fixed before outcomes.                                                                                                                      |

Do not add post-task perceived difficulty, number of queries, or verification behavior as controls in the primary treatment models. These may be outcomes of the treatment itself. Task variants repeat across matched allocation triplets. Use shared template/category and recorded parameters; account for the matching when feasible.

**Multiple testing:** preregister H1–H3 as the primary family. Apply Holm correction across the six primary directional contrasts listed above: two for H1, two for H2, and two for H3. Report estimates and two-sided confidence intervals as well. Use Benjamini–Hochberg at q = .05 for the prespecified secondary test family, including the maximum of the two one-sided p-values for each equivalence comparison. Keep purely descriptive H7 summaries outside confirmatory claims.

For robustness, report success uncertainty bounds, technical-failure rates, missingness by group, and results with versus without documented protocol violations. If a mixed model fails with the small sample, use prespecified participant-summary and allocation-triplet-adjusted analyses rather than trying many models until one is significant. Do not use a test of demographic balance as proof that assignment removed confounding; report allocation records and descriptive balance.

### Missing data and exclusions

Timeouts, wrong answers, and “could not find one” responses stay in the main outcome data. A single attention-check failure is flagged, not an automatic exclusion. Leaving oTree to use permitted websites is expected. Report observed outside-tool violations and provide a sensitivity analysis; do not silently drop them from the main assigned-group comparison.

Distinguish technical missingness from task failure. An ordinary working-tool timeout is a task outcome; a server crash that prevents participation is missing technical data. Keep unaffected attempts, report affected counts by group, and prespecify handling before collection. For participant-level productivity, report complete-battery results alongside sensitivity bounds for missing attempts; do not let missing tasks silently shorten the denominator. Withdrawals and participants who never begin scored tasks are reported in the participant flow.

## 12. Risks, limits, and practical responses

| Issue                                       | Response                                                                                                                                                       |
|---------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Three groups and a small classroom           | Check detectable effects before launch. Treat estimates as pilot evidence if precision is limited; do not promise population-wide findings.                    |
| Web filter fails or Google changes          | Test before the session. Pause the affected procedure rather than silently replacing search with another product or untested extension.                        |
| AI configuration changes or service is slow | Record settings and response times; use the same configuration in A/B. Do not switch models partway without documenting a protocol deviation.                  |
| Price, availability, or rating changes      | Retain task-time evidence and review promptly. Mark unresolved facts unknown and report uncertainty by group.                                                  |
| Task becomes infeasible                     | Check before launch and record later concerns. Do not decide infeasibility merely because participants failed; investigate independently of group performance. |
| Outside tool use or copying                 | Standardized instructions, individual tasks, supervised room, and consented browser recordings. Do not claim guaranteed prevention.                            |
| Recording privacy                           | No audio/webcam; clean browser profiles; coded filenames; restricted access and an approved deletion schedule. Avoid capturing personal accounts.              |
| Mechanism claims exceed evidence            | Code only visible actions and supported errors. Treat mediation and behavioral associations as exploratory.                                                    |
| Live web limits scoring and concentration   | Report unknown facts and changing choice opportunities. No global optimality claims or identical-task concentration claims.                                    |

This is a classroom experiment with balanced deterministic allocation using live websites. It is not a representative consumer field experiment. It measures short-run performance on constrained tasks, not purchases, long-term learning, or open-ended shopping preferences. The theoretical contribution will depend on the results and a separate literature review; this proposal does not claim to be the first study of its kind.

## 13. Decisions to finalize before collection

1.  Confirm the class size and session date; divide students as evenly as possible across the three groups and report the study as a classroom pilot.
2.  Choose and test the exact AI model, live-web access, browser configuration, location setting, and recording method.
3.  Validate individualized task parameters and four-minute limits with a small usability pilot.
4.  Approve consent, recording access/retention, participation alternative, payment amounts, and bonus-payment schedule.
5.  Finalize the scoring manual, reviewer training, uncertainty rules, and equivalence margin.
6.  Test simultaneous usage, external-tab deadlines, refresh recovery, evidence linkage, and exports.
7.  Lock hypotheses, contrasts, multiplicity rules, missing-data handling, sample stopping rule, and deviations procedure in the preregistration.

Before data collection, the team will complete an end-to-end test covering participant assignment, all task pages, external tool access, deadlines, evidence collection, scoring, and data export.

## References

1.  [Google Search Help: AI Overviews and the Web filter](https://support.google.com/websearch/answer/14901683?hl=en). Checked September 29, 2026.
2.  [oTree documentation: Live pages, event storage, and asynchronous API calls](https://otree.readthedocs.io/en/latest/live.html). Consulted for implementation feasibility.
3.  [MDN: Same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Same-origin_policy). Consulted for limits on observing external website activity.

</div>
