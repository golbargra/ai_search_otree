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

**For this class, use the instructor's laptop as the local server. No paid cloud hosting is required.** Students open the laptop's network address from their own devices. Google and ChatGPT still require internet access. The laptop serves oTree pages and stores the local database. This setup must pass a rehearsal on the classroom network; the automated participant-flow tests are not a simultaneous capacity test.

### Windows / PowerShell local setup

Install the dependencies ahead of class. Open PowerShell in this repository and run:

```powershell
pip install -r requirements.txt
$env:OTREE_ADMIN_PASSWORD = Read-Host "Choose an admin password"
$env:OTREE_SECRET_KEY = [guid]::NewGuid().ToString('N') + [guid]::NewGuid().ToString('N')
$env:OTREE_PRODUCTION = "1"
otree prodserver 8000
```

Keep this window open. In this installed oTree version, `prodserver` listens on all network interfaces. Open `http://localhost:8000` on the instructor laptop and sign in. Use Rooms → classroom → Create session. Select `ai_search_70` for 70 people, or `ai_search` with 69 for exact 23/23/23 allocation.

In another PowerShell window run `ipconfig`. Find the IPv4 address of the active classroom Wi-Fi or Ethernet adapter, not a VPN or virtual adapter. For example, if it is `192.168.1.25`, students open:

```text
http://192.168.1.25:8000/room/classroom/
```

Use the actual address. `localhost` only works on the instructor laptop. For individual links from the admin page, replace the `localhost:8000` portion with the laptop's IP address and port, preserving the rest of each URL.

Allow Python/oTree through Windows Firewall for the classroom network or ask IT for a scoped inbound rule for TCP port 8000. Do not disable the firewall. Keep the laptop plugged in, prevent sleep while plugged in, and do not close the lid or terminal during collection. Use the same server process and secret key throughout the session. With no `DATABASE_URL`, this local setup uses oTree's local SQLite database; preserve `db.sqlite3`, export the data, and do not reset it after collection. If returning on another day, restore the same private secret key rather than generating a new one.

**Critical check:** campus Wi-Fi may block connections between student devices and the instructor laptop even when both are on the same network. Test from a second device in the actual classroom before class day. If blocked, ask campus IT for a permitted lab network or a network arrangement that allows local TCP/WebSocket traffic. An allowed private router can be an alternative only if student devices can reach the laptop and still access Google/ChatGPT. A phone hotspot is not a dependable plan for 70 devices. If no available network allows devices to reach the laptop, a shared local session cannot run until that connectivity is resolved.

Other no-cloud options include a campus lab computer acting as the server on a permitted lab network, or another instructor laptop on the same reachable network. Internet access remains necessary for the external search and AI tasks.

### Rehearsal before class

1. Start this version on the instructor laptop and create a separate test session on the actual classroom network.
2. Use oTree browser bots or a browser load harness with at least 70 concurrent participants (ideally 80 for headroom). Exercise page transitions, live autosave messages, simultaneous final submissions, and exports. Command-line bot success is not a load test.
3. Test deadlines, tab switching, refresh recovery, and timeout handling on actual student browsers. Suggested acceptance criteria: no server errors or lost submitted records, responsive pages (e.g. under two seconds in normal conditions), and consistent exported assignments and task counts.
4. Run a short real-device rehearsal on campus Wi-Fi. Check Google Web results, retailer pages, pop-ups, and ChatGPT login, model/web access, and account limits. About 46–47 students may use ChatGPT at once, each through their own permitted access. Avoid sharing one personal ChatGPT account.
5. Arrange screen recording separately if the consent says it occurs. The app's consent currently states that the browser is recorded; align that statement with the actual approved collection process before students see it. Test evidence filenames and collection. Verify every task variant has qualifying live products.
6. Use individual participant links or a room with secure anonymous participant labels to reduce duplicate entries. The existing unlabeled room-wide link is convenient but a second browser can occupy another slot. Keep any code-to-name roster separate from research exports.

### On class day

On the instructor laptop, create a fresh session in **Rooms → classroom**, selecting `ai_search` with a multiple of three or `ai_search_70` with 70. Distribute the actual session participant links once per student, or the configured room URL:

```text
http://YOUR-LAPTOP-IP:8000/room/classroom/
```

Students can all participate at once and work at their own pace. There is no waiting for other participants between tasks. Keep the server running until everyone finishes. If someone disconnects, reopen their existing participant link; do not allocate a second slot. The task deadline continues during external browsing or a disconnect, and only drafts that reached the server can be recovered.

## Export and payment

Download **ai_search** (answers, surveys, assignments and timing) and **ai_search custom** (events) from the admin Data page, and check participant/arm counts before closing the server. Keep task-time evidence for later verification.

The displayed planning payment is $5 participation plus $0.50 per verified correct scored task, maximum **$6.50** for three tasks. Confirm the team's actual approved payment before collection. Bonuses are verified and paid later, not calculated automatically by oTree.

The earlier PDF quick guide predates this update; use this README for the current design and hosting procedure.

Official deployment references: [oTree Heroku setup and performance](https://otree.readthedocs.io/en/latest/server/heroku.html), [Linux/Postgres server setup](https://otree.readthedocs.io/en/latest/server/ubuntu.html), and [rooms and participant links](https://otree.readthedocs.io/en/latest/rooms.html).
