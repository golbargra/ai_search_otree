# AI Product-Search Experiment — oTree App

A scaffold implementation of the AI Product-Search study on the oTree
platform. Four-arm between-subjects design: **S** (Search-only), **D**
(Search + AI Overview), **A** (AI-only), **B** (AI + Search).

## Structure

```
ai_search_otree/
├── settings.py                   # oTree project settings
├── requirements.txt
├── README.md                     # this file
└── ai_search/                    # the app
    ├── __init__.py               # models, pages, page sequence (oTree 5.x)
    ├── task_bank.py              # task templates + anchor tasks
    ├── static/ai_search/
    │   └── focus_tracker.js      # client-side focus + log tracking
    └── templates/ai_search/
        ├── Consent.html
        ├── PreSurvey.html
        ├── Instructions.html
        ├── Comprehension.html
        ├── Task.html
        ├── MicroSurvey.html
        ├── PostSurvey.html
        └── Results.html
```

## Quick start

```bash
# 1. Install oTree (Python 3.10+)
pip install -r requirements.txt

# 2. From this folder, run the dev server
otree devserver

# 3. Open the printed URL in your browser and click through as a demo participant
```

## Page flow

1. **Consent** — IRB consent and study description
2. **PreSurvey** — demographics, PS1–PS4, AI literacy items, attention check
3. **Instructions** — task format + your assigned tool
4. **Comprehension** — 3-item check (must pass to continue)
5. **Task** (repeated 1 + 10 rounds) — practice + 10 scored tasks; enforces
   the assigned tool via which iframes are rendered
6. **MicroSurvey** — confidence + difficulty per task
7. **PostSurvey** — tool-specific perceptions, workload, open-text
8. **Results** — earnings summary and Prolific redirect

## What's real vs stubbed

- **Real:** arm assignment, page sequence, data model, task generation,
  focus/blur tracking, revision counting, answer scoring against
  reported values.
- **Stubbed (needs custom development for a real study):**
  - Google search results are shown via an iframe; production would use
    a proxy that logs `?q=` query strings server-side rather than
    trusting the participant's browser
  - ChatGPT interactions run against the public chat.openai.com iframe;
    production would either (a) proxy through the OpenAI API with logged
    turns, or (b) require participants to paste their transcript
  - Catalog verification is stubbed to check the participant's own
    reported fields. Production should call a rolling catalog snapshot
    (via retailer APIs or scrape) at submission time and score against
    that.
  - Screen recording (MediaRecorder API) is not implemented; a
    production build should trigger it for the audit subsample.

## Data export

`otree devserver` provides an admin panel at `/DemoDataExport`. Each
round writes: `arm`, `task_id`, `time_sec`, `n_met`, `success`,
`query_log`, `ai_log`, `focus_lost`, plus the micro-survey ratings.
Participant-level fields (pre-survey, post-survey, total earnings) are
in the participant export.

## Extending

- **Blocked randomization on prior AI experience:** move arm assignment
  from `creating_session()` into a `WaitPage` after `PreSurvey`, so the
  pre-survey answer can drive the block.
- **Real catalog snapshots:** build a separate cron job that pulls
  anchor-task product lists every 30 min and stores them in a database
  the `score_answer()` function reads from.
- **Screen recording:** use the browser's MediaRecorder API in the
  Task template; upload chunks to the oTree custom `live_method`.
