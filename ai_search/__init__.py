"""
AI Product-Search Experiment — oTree app skeleton
=================================================

Between-subjects, four-arm design:
  S = Search-only (Google, udm=14 Web filter)
  D = Search + AI Overview (Google default view)
  A = AI-only (ChatGPT)
  B = AI + Search (both panes)

Each participant:
  1. Consent
  2. Pre-survey (demographics, AI experience, AI literacy, attention check)
  3. Instructions
  4. Comprehension gate (loops until passed)
  5. Practice task (unscored)
  6. Scored task battery (10 tasks: 3 anchor + 7 individualized)
     Each task followed by a two-item micro-survey.
  7. Post-experiment survey (perception, workload, open text)
  8. Results & payment

This file follows the modern oTree 5.x single-file layout.
"""
import json
import random
import time

from otree.api import (
    BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Page, WaitPage, models, ExtraModel,
)

from . import task_bank


# =====================================================================
# CONSTANTS
# =====================================================================
class C(BaseConstants):
    NAME_IN_URL = 'ai_search'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1 + task_bank.N_TASKS_PER_BATTERY  # 1 practice + 10 scored

    ARMS = ['S', 'D', 'A', 'B']
    ARM_LABELS = {
        'S': 'Search-only (Web filter, no AI Overview)',
        'D': 'Search + AI Overview (Google default)',
        'A': 'AI-only (ChatGPT)',
        'B': 'AI + Search (both tools)',
    }
    BASE_PAY = 8.00                 # completion base rate ($)
    BONUS_PER_CORRECT = 0.50        # bonus per fully correct scored task ($)
    BONUS_CAP = 5.00                # maximum bonus


# =====================================================================
# MODELS
# =====================================================================
class Subsession(BaseSubsession):

    def creating_session(self):
        """
        Called once per session at creation. Assigns arm and battery to
        every player. Assignment is BLOCKED on self-reported prior AI
        experience if available (falls back to random if pre-survey has
        not been submitted).
        """
        if self.round_number != 1:
            return
        for p in self.get_players():
            # Deterministic seed per participant for reproducibility
            seed = p.participant.id_in_session * 9973 + self.session.id
            rng = random.Random(seed)
            # Simple random arm assignment; production version should
            # implement stratified/blocked assignment.
            p.participant.vars['arm'] = rng.choice(C.ARMS)
            p.participant.vars['battery'] = task_bank.build_battery(seed)
            p.participant.vars['practice_task'] = task_bank.get_practice_task()
            p.participant.vars['n_correct'] = 0


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    # -------- Pre-survey ---------------------------------------------
    age_band  = models.StringField(
        choices=['18-24', '25-34', '35-49', '50-65'],
        label="What is your age?", blank=True)
    gender    = models.StringField(blank=True, label="Gender (self-describe)")

    ps1 = models.IntegerField(min=1, max=5, blank=True,
        label="How familiar are you with AI chat tools (ChatGPT, Gemini, Claude)?")
    ps2 = models.IntegerField(min=1, max=5, blank=True,
        label="In the past month, how often did you use an AI chat tool?")
    ps3 = models.IntegerField(min=1, max=5, blank=True,
        label="How often do you use AI to find or choose a product to buy?")
    ps4 = models.IntegerField(min=1, max=5, blank=True,
        label="How would you rate your ability to get useful results from AI tools?")

    ai_lit_1 = models.BooleanField(blank=True,
        label="AI chat tools can state incorrect facts confidently. True or False?")
    ai_lit_2 = models.StringField(blank=True,
        choices=['retailer page', 'AI chat', 'social media'],
        label="Which is most reliable for a product's current price?")
    ai_lit_3 = models.BooleanField(blank=True,
        label="If an AI gives a product's review count, that number is always current. True or False?")

    attention_check = models.StringField(blank=True,
        choices=['Never', 'Rarely', 'Sometimes', 'Often', 'Very often'],
        label="To show you are reading, select 'Often' here.")

    shop_freq = models.IntegerField(min=1, max=5, blank=True,
        label="How often do you shop online?")

    # -------- Comprehension gate -------------------------------------
    comp_score = models.IntegerField(initial=0)

    # -------- Per-round task state -----------------------------------
    task_id       = models.StringField(blank=True)
    task_json     = models.LongStringField(blank=True)   # full task params
    is_practice   = models.BooleanField(initial=False)

    start_ts      = models.FloatField(blank=True)
    submit_ts     = models.FloatField(blank=True)
    time_sec      = models.FloatField(blank=True)

    # Participant's submitted answer
    ans_product_name = models.StringField(blank=True)
    ans_url          = models.StringField(blank=True)
    ans_retailer     = models.StringField(blank=True)
    ans_price        = models.FloatField(blank=True)
    ans_rating       = models.FloatField(blank=True)
    ans_reviews      = models.IntegerField(blank=True)

    # Auto-scored outcomes
    n_met            = models.IntegerField(blank=True)   # 0..k constraints met
    success          = models.BooleanField(blank=True)

    # Process metrics
    n_queries        = models.IntegerField(initial=0)
    n_ai_turns       = models.IntegerField(initial=0)
    n_revisions      = models.IntegerField(initial=0)
    focus_lost       = models.IntegerField(initial=0)
    query_log        = models.LongStringField(blank=True)  # JSON
    ai_log           = models.LongStringField(blank=True)  # JSON

    # Micro-survey (per task)
    micro_confidence = models.IntegerField(min=1, max=7, blank=True,
        label="How confident are you that your answer is correct?")
    micro_difficulty = models.IntegerField(min=1, max=7, blank=True,
        label="How difficult was this task?")

    # -------- Post-experiment survey ---------------------------------
    post_easy       = models.IntegerField(min=1, max=7, blank=True,
        label="This tool made the tasks easy.")
    post_trust      = models.IntegerField(min=1, max=7, blank=True,
        label="I trusted the answers this tool gave me.")
    post_reuse      = models.IntegerField(min=1, max=7, blank=True,
        label="I would use this tool again for this kind of search.")
    post_bias       = models.IntegerField(min=1, max=7, blank=True,
        label="The results from this tool felt biased or sponsored-influenced.")
    post_faster     = models.IntegerField(min=1, max=7, blank=True,
        label="This tool helped me finish faster.")
    tlx_mental      = models.IntegerField(min=1, max=7, blank=True,
        label="Mental demand of the study overall.")
    tlx_effort      = models.IntegerField(min=1, max=7, blank=True,
        label="Effort required overall.")
    tlx_frustration = models.IntegerField(min=1, max=7, blank=True,
        label="Frustration overall.")
    open_text_1 = models.LongStringField(blank=True,
        label="What made a task easy or hard?")
    open_text_2 = models.LongStringField(blank=True,
        label="Was anything confusing or unclear?")


# =====================================================================
# HELPERS
# =====================================================================
def is_practice_round(round_number):
    return round_number == 1


def get_task_for_round(player):
    """Return the task dict assigned to this player for this round."""
    if is_practice_round(player.round_number):
        return player.participant.vars['practice_task']
    battery = player.participant.vars['battery']
    idx = player.round_number - 2  # rounds 2..N are scored
    return battery[idx]


def score_answer(player, task):
    """
    Verify the participant's submitted answer against the task constraints.
    In a production deployment this would call a catalog snapshot; here we
    check the participant's own reported product fields — the same fields
    are captured in `tool_log` / screen recording for later audit.
    """
    constraints = [
        ('price', task['price_min'] <= (player.ans_price or 0) <= task['price_max']),
        ('rating', (player.ans_rating or 0) >= task['min_rating']),
        ('reviews', (player.ans_reviews or 0) >= task['min_reviews']),
        ('has_url', bool((player.ans_url or '').strip())),
    ]
    n = sum(1 for _, ok in constraints if ok)
    player.n_met = n
    player.success = (n == len(constraints))


# =====================================================================
# PAGE CLASSES
# =====================================================================
class Consent(Page):
    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self, timeout_happened=False):
        # store arm on the player for easier export
        pass


class PreSurvey(Page):
    form_model = 'player'
    form_fields = [
        'age_band', 'gender',
        'ps1', 'ps2', 'ps3', 'ps4',
        'ai_lit_1', 'ai_lit_2', 'ai_lit_3',
        'attention_check', 'shop_freq',
    ]

    def is_displayed(self):
        return self.round_number == 1

    def error_message(self, values):
        if values.get('attention_check') != 'Often':
            return "Attention check failed. Please read the item carefully."


class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        arm = self.participant.vars.get('arm', 'S')
        return dict(arm=arm, arm_label=C.ARM_LABELS[arm])


class Comprehension(Page):
    form_model = 'player'
    form_fields = ['comp_score']

    def is_displayed(self):
        return self.round_number == 1

    def error_message(self, values):
        if values.get('comp_score', 0) < 3:
            return "You need to get all comprehension items correct. Please review the instructions."


class Task(Page):
    """
    Displays the current task and the assigned tool panes.
    The template uses `arm` to decide which iframes / chat pane to render.
    All actions (queries, AI turns, focus loss, revisions) are POSTed
    back via JS calls; here we accept the final submitted answer.
    """
    form_model = 'player'
    form_fields = [
        'ans_product_name', 'ans_url', 'ans_retailer',
        'ans_price', 'ans_rating', 'ans_reviews',
        'query_log', 'ai_log',
        'n_queries', 'n_ai_turns', 'n_revisions', 'focus_lost',
    ]

    def is_displayed(self):
        return True

    def vars_for_template(self):
        task = get_task_for_round(self.player)
        self.player.task_id     = task['task_id']
        self.player.task_json   = json.dumps(task)
        self.player.is_practice = is_practice_round(self.round_number)
        self.player.start_ts    = time.time()
        return dict(
            task=task,
            arm=self.participant.vars.get('arm', 'S'),
            arm_label=C.ARM_LABELS[self.participant.vars.get('arm', 'S')],
            round_number=self.round_number,
            n_total=C.NUM_ROUNDS,
            is_practice=is_practice_round(self.round_number),
        )

    def before_next_page(self, timeout_happened=False):
        self.player.submit_ts = time.time()
        if self.player.start_ts:
            self.player.time_sec = self.player.submit_ts - self.player.start_ts
        task = get_task_for_round(self.player)
        score_answer(self.player, task)
        if self.player.success and not self.player.is_practice:
            self.participant.vars['n_correct'] = self.participant.vars.get('n_correct', 0) + 1


class MicroSurvey(Page):
    form_model = 'player'
    form_fields = ['micro_confidence', 'micro_difficulty']

    def is_displayed(self):
        # After every task including the practice
        return True


class PostSurvey(Page):
    form_model = 'player'
    form_fields = [
        'post_easy', 'post_trust', 'post_reuse', 'post_bias', 'post_faster',
        'tlx_mental', 'tlx_effort', 'tlx_frustration',
        'open_text_1', 'open_text_2',
    ]

    def is_displayed(self):
        return self.round_number == C.NUM_ROUNDS


class Results(Page):
    def is_displayed(self):
        return self.round_number == C.NUM_ROUNDS

    def vars_for_template(self):
        n_correct = self.participant.vars.get('n_correct', 0)
        bonus = min(C.BONUS_CAP, n_correct * C.BONUS_PER_CORRECT)
        total = C.BASE_PAY + bonus
        return dict(
            n_correct=n_correct,
            bonus=f"{bonus:.2f}",
            total=f"{total:.2f}",
            base=f"{C.BASE_PAY:.2f}",
        )


# =====================================================================
# PAGE SEQUENCE
# =====================================================================
page_sequence = [
    Consent,
    PreSurvey,
    Instructions,
    Comprehension,
    Task,
    MicroSurvey,
    PostSurvey,
    Results,
]
