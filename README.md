# AI Product-Search Study

An oTree classroom study with three arms: **S: Search only**, **A: ChatGPT only**, and **B: ChatGPT and Search**. Google uses the Web filter (`udm=14`). Each participant does one unscored practice task and **three scored tasks**, one easy, one medium, and one hard. Allow about **30–35 minutes**.

## What the code does

`settings.py` defines sessions, timers, payment display, and the classroom room. `ai_search/__init__.py` contains models, allocation, consent, surveys, comprehension retries, tasks, timing, logging, and exports. `task_bank.py` defines six candidate categories and finite variants; only three categories are selected per person. Templates show the pages, tool launchers, and answer form. `tests.py` contains the automated participant flow.

Flow: Consent → Background → Knowledge → assigned instructions → comprehension (up to three attempts) → practice → three Task/Rating rounds → Post-survey → Completion. Students progress independently; there are no group wait pages.

ChatGPT and Google open in external tabs. There is **no AI API**, embedded assistant, automatic correctness scoring, or screen recorder. Reviewers check product claims afterward. The custom event export captures launcher activity and focus changes, not complete external browsing or chat transcripts.

## Equal assignment and a class of 70

Arms are assigned once at session creation in a fixed S/A/B cycle, stored in every round, and revealed after baseline questions. Assignment does not depend on survey completion speed or AI-use answers.

| Session config | Participant count | Assigned arms |
|---|---:|---|
| `ai_search` (exact equality required) | 69 | 23 / 23 / 23 |
| `ai_search` (exact equality required) | 72 | 24 / 24 / 24 |
| `ai_search_70` (near equality permitted) | 70 | 24 / 23 / 23 |

The equal config rejects counts not divisible by three. The near-equal config accepts other sizes too and keeps assigned counts within one. Seventy people cannot be divided exactly equally among three arms. If all 70 should participate, use `ai_search_70`; do not discard a student's completed data just to make counts equal. Do not create 72 slots and assume 70 arrivals will fill every arm equally.

These counts describe assigned slots, not guaranteed completions. Withdrawals, unused links, and failed comprehension checks can produce unequal final samples. Monitor and report these outcomes by arm.

Consecutive triplets share a seed, task categories, variants, and order, with one slot per arm. Batteries vary across triplets. This balances tasks as well as arms when all slots are used. Supervise individual work because some task requirements repeat.

A fixed cycle is not randomized allocation. Arrival order could correlate with condition when using the room-wide link. For stronger causal inference, a randomly shuffled allocation with fixed equal quotas is preferable; it preserves exact counts. The implemented cycle follows the requested nonrandom assignment.

## Try it locally

Install Python 3.10 or newer, open a terminal in this folder, then run:

```bash
pip install -r requirements.txt
otree devserver
```

Open `http://localhost:8000`. Use the three-participant `ai_search` demo to inspect all arms. Keep the existing `_static` folder. Use a fresh test database when checking an updated version; do not reset a database containing study data.

For automated flow checks:

```bash
pip install -r requirements-test.txt
otree test ai_search 3
otree test ai_search 69
otree test ai_search_70 70
```

These command-line bots check forms and flow. They do not measure simultaneous browser traffic or external Google/ChatGPT availability.

## Hosting about 70 students at once

**Recommended:** use oTree Hub to deploy to a paid Heroku production server with Postgres, or use an existing university oTree server maintained by IT. The present app makes lightweight survey and event requests; Google and ChatGPT traffic goes directly from students' browsers to those providers. There is no shared AI API queue on the oTree server. This architecture is suitable to test for 70 concurrent students, but no capacity guarantee follows from participant count alone.

| Option | Advantages | What to check |
|---|---|---|
| oTree Hub / paid Heroku | Public HTTPS link; deployment and monitoring support | Hosting/database tier, WebSockets, and tested capacity; follow oTree's guidance to use one web dyno and upgrade its size if needed |
| University production server | Existing support, network access, and data arrangements | Supported oTree version, Postgres, HTTPS, WebSockets, and IT availability during class |
| Laptop on classroom network | Convenient for a small rehearsal | Firewall, campus client isolation, sleep, database contention, and network stability; use for class only after a full load rehearsal |

Do not use `otree devserver` for the live class. On a managed Linux server use `otree prodserver 8000`, Postgres configured through `DATABASE_URL`, production mode, a private admin password, and a strong `OTREE_SECRET_KEY`. A reverse proxy must support WebSockets. Let IT or oTree Hub manage the actual setup.

### Rehearsal before class

1. Deploy this version to a separate test session on the intended host.
2. Use oTree browser bots or a browser load harness with at least 70 concurrent participants (ideally 80 for headroom). Exercise page transitions, live autosave messages, simultaneous final submissions, and exports. Command-line bot success is not a load test.
3. Test deadlines, tab switching, refresh recovery, and timeout handling on actual student browsers. Suggested acceptance criteria: no server errors or lost submitted records, responsive pages (e.g. under two seconds in normal conditions), and consistent exported assignments and task counts.
4. Run a short real-device rehearsal on campus Wi-Fi. Check Google Web results, retailer pages, pop-ups, and ChatGPT login, model/web access, and account limits. About 46–47 students may use ChatGPT at once, each through their own permitted access. Avoid sharing one personal ChatGPT account.
5. Arrange screen recording separately if the consent says it occurs. The app's consent currently states that the browser is recorded; align that statement with the actual approved collection process before students see it. Test evidence filenames and collection. Verify every task variant has qualifying live products.
6. Use individual participant links or a room with secure anonymous participant labels to reduce duplicate entries. The existing unlabeled room-wide link is convenient but a second browser can occupy another slot. Keep any code-to-name roster separate from research exports.

### On class day

Create a fresh session in **Rooms → classroom**, selecting `ai_search` with a multiple of three or `ai_search_70` with 70. Distribute the actual session participant links once per student, or the configured room URL:

```text
https://YOUR-HOST/room/classroom/
```

Students can all participate at once and work at their own pace. There is no waiting for other participants between tasks. Keep the server running until everyone finishes. If someone disconnects, reopen their existing participant link; do not allocate a second slot. The task deadline continues during external browsing or a disconnect, and only drafts that reached the server can be recovered.

## Export and payment

Download **ai_search** (answers, surveys, assignments and timing) and **ai_search custom** (events) from the admin Data page, and check participant/arm counts before closing the server. Keep task-time evidence for later verification.

The displayed planning payment is $5 participation plus $0.50 per verified correct scored task, maximum **$6.50** for three tasks. Confirm the team's actual approved payment before collection. Bonuses are verified and paid later, not calculated automatically by oTree.

The earlier PDF quick guide predates this update; use this README for the current design and hosting procedure.

Official deployment references: [oTree Heroku setup and performance](https://otree.readthedocs.io/en/latest/server/heroku.html), [Linux/Postgres server setup](https://otree.readthedocs.io/en/latest/server/ubuntu.html), and [rooms and participant links](https://otree.readthedocs.io/en/latest/rooms.html).
