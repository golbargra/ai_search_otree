# AI Product-Search Experiment (classroom pilot) - oTree

Implements `docs/AI_Product_Search_Proposal.md`: four between-subjects groups, one practice
task plus six scored product-search tasks, surveys, and data exports.

| Group | Tools | How it works in oTree |
|---|---|---|
| S | Google, Web filter | Search box on the task page opens `google.com/search?udm=14&q=...` in a new tab |
| D | Google, default view | Search box opens `google.com/search?q=...` (AI Overviews may appear) |
| A | ChatGPT only | Button opens the public ChatGPT website in a new tab |
| B | ChatGPT + Google Web filter | Both of the above |

## Session flow
Consent -> Background survey -> AI-limitations knowledge (3 items) -> **group assigned** ->
Instructions (group-specific) -> Comprehension check (up to 3 tries; feedback on try 2,
standard clarification on try 3; if still wrong, no scored tasks) -> Practice task (3 min) ->
6 x [Start page -> Task (4 min) -> Ratings] -> Post-survey -> Completion.

## Run it
```bash
pip install -r requirements.txt
otree devserver          # test at http://localhost:8000
otree test ai_search 8   # automated bot run-through
```
For class, use `otree prodserver` (or oTree Hub/Heroku). Set `OTREE_ADMIN_PASSWORD`,
`OTREE_SECRET_KEY`, and `OTREE_PRODUCTION=1`. Create a session in the **classroom** room
with the number of students, and give students the room link.

Settings you may change in `settings.py`: `task_seconds` (240), `practice_seconds` (180),
`ai_url` (https://chatgpt.com/), `participation_fee` (5), `bonus_per_correct` (0.50),
`max_total_pay` (8).

## What is implemented from the proposal
- **Assignment:** blocks of four (S/D/A/B shuffled) within two strata of PS2 prior AI use
  (never / less than weekly vs weekly or more), done after baseline items. Stored as
  `arm` and `randomization_block` (e.g. `low-2`).
- **Tasks:** `task_bank.py`. Each student gets all 6 categories (2 easy, 2 medium, 2 hard);
  each category uses one of 3 prechecked variants; order shuffled; seed saved (`participant.seed`).
- **Timing:** server-side deadline set when requirements are revealed; the same deadline
  holds after a refresh; late submissions count as timeouts. Draft answers autosave and are
  restored after refresh; on timeout the draft is kept (`draft_json`) but not counted as submitted.
- **Answer form:** product, variant, retailer, seller, URL, price, rating, rating count,
  stock, extra attribute, each with "Could not verify"; "I could not find one" button.
- **Surveys:** wording from Section 8, incl. attention check ("Sometimes"), category
  familiarity, per-task confidence (only if submitted) / difficulty / effort, post-survey with
  "Cannot judge" (coded -1), workload items, open text, B-only tool question.
- **No automatic scoring.** oTree stores what students report; reviewers verify later.

## Data exports (Admin -> Data)
- **ai_search (per app)**: one row per student x round (round 1 = practice, rounds 2-7 =
  scored): `arm, randomization_block, task_order, task_id, template_id, difficulty,
  task_params, start_ts, end_ts, time_sec, submitted, no_answer, timed_out, ans_*,
  confidence, difficulty_rating, effort_rating, n_launcher_queries, n_chatgpt_opens,
  first_action_sec, focus_lost`. Pre-survey answers are in round 1, post-survey in round 7.
- **ai_search custom export**: event log (launcher searches with query text, ChatGPT opens,
  focus lost/back, task end) with seconds into the task.
- Reviewer scoring (`verified_success`, `constraint_status_*`, ...) goes in a separate sheet
  keyed by `participant.code` + `task_id`, merged for analysis.

## Deviations from the proposal (report these)
1. **ChatGPT is the public website, not an API assistant inside oTree.** oTree cannot see
   ChatGPT messages, so `n_ai_turns`, `ai_transcript`, and the model used must come from
   screen recordings. oTree cannot stop S/D students from opening ChatGPT on their own;
   compliance relies on instructions and recordings.
2. Only searches typed into the oTree launcher are logged; later searches inside the Google
   tab come from recordings (missing, not zero, if footage is incomplete).
3. `focus_lost` also counts refreshes and tab switches; never use it for exclusion.

## Before-class checklist
- [ ] Check all 18 task variants (+ practice) on the live web; delete infeasible ones in `task_bank.py`.
- [ ] On a lab computer: Web-filter link shows no AI Overview; default Google works; ChatGPT
      opens with web search. Decide logged-in (study accounts) vs logged-out ChatGPT; same for everyone.
- [ ] Allow pop-ups from the oTree site in the study browser (tools open in new tabs).
- [ ] Clean browser profiles, same location/language; note settings in session notes.
- [ ] Screen recording set up and linked to each student's study code (shown on completion page).
- [ ] Fill in consent details (payment, recording retention) in `Consent.html`.
- [ ] Full dry run with 4+ people, then export and check the data.
