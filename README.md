# How to Run the AI Product-Search Study

**Quick guide for the oTree app (`ai_search_otree`)**

## 1. One-time setup

Do this on the laptop that will run the study.

1.  Install Python (3.10 or newer) from python.org.
2.  Unzip `ai_search_otree.zip`.
3.  Open Terminal (Mac) or Command Prompt (Windows) and run:

``` bash
cd path/to/ai_search_otree
pip install otree
```

## 2. Try it yourself first

1.  Run:

``` bash
otree devserver
```

2.  Open `http://localhost:8000` in your browser.
3.  Click **ai_search** under **Demo**, click a participant link, and go
    through the study as a student.
4.  To stop, press `Ctrl + C` in the terminal.

## 3. On class day

1.  Connect the laptop to the same Wi-Fi as the students.
2.  Start the study server.

### Mac

``` bash
export OTREE_ADMIN_PASSWORD=pick_a_password
export OTREE_PRODUCTION=1
otree prodserver 8000
```

### Windows

``` cmd
set OTREE_ADMIN_PASSWORD=pick_a_password
set OTREE_PRODUCTION=1
otree prodserver 8000
```

3.  Find the laptop's IP address:

    -   **Mac:** System Settings \> Wi-Fi \> Details
    -   **Windows:** type `ipconfig` and look for **IPv4 Address**.

    It looks like `192.168.1.25`.

4.  On the laptop, open `http://localhost:8000`, log in as admin with
    your password, then go to **Rooms \> classroom \> Create session**.
    Enter the number of students and click **Create**.

5.  Write this link on the board, using your laptop's IP:

``` text
http://192.168.1.25:8000/room/classroom
```

6.  Students open the link and follow the screens. Keep the laptop on
    and awake until everyone finishes.

## 4. Get the data

1.  On the laptop, open `http://localhost:8000` \> **Data**.
2.  Download both files:
    -   **ai_search** --- answers, times, surveys
    -   **ai_search custom** --- search and ChatGPT activity log
3.  Only after the files are saved, stop the server with `Ctrl + C`.

## If something goes wrong

-   **Students can't open the link:** Check that they are on the same
    Wi-Fi and allow Python through the laptop's firewall.
-   **Google or ChatGPT won't open:** Allow pop-ups for the study site
    in the browser.
-   **A student refreshes the page:** That's fine. Their timer and typed
    answers stay.
