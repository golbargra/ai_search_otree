"""
AI product-search experiment (classroom pilot) - oTree app.

Groups (between-subjects, fixed for the whole session):
  S = Google with the Web filter (udm=14), no AI
  D = Default Google (AI Overviews may appear)
  A = ChatGPT only (public website, opened in a new tab)
  B = ChatGPT + Google Web filter

Round 1 = consent, surveys, assignment, instructions, comprehension, practice.
Rounds 2-7 = six scored tasks (4 minutes each) + ratings after each.
Last round also shows the post-survey and the completion page.

oTree records answers only. Correctness is verified later by reviewers.
"""
import json
import random
import time

from otree.api import *

from . import task_bank

doc = "AI product-search experiment (four groups, six tasks)."


class C(BaseConstants):
    NAME_IN_URL = 'ai_search'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1 + task_bank.N_SCORED_TASKS  # practice + 6 scored
    ARMS = ['S', 'D', 'A', 'B']
    ARM_LABELS = {
        'S': 'Google search (Web filter)',
        'D': 'Google search (default view)',
        'A': 'ChatGPT',
        'B': 'ChatGPT and Google search (Web filter)',
    }
    GOOGLE_WEB = 'https://www.google.com/search?udm=14&q='
    GOOGLE_DEFAULT = 'https://www.google.com/search?q='
    CANNOT_JUDGE = -1


# ---------------------------------------------------------------- helpers
FREQ = [[1, 'Never'], [2, 'Less than weekly'], [3, 'One or two days a week'],
        [4, 'Three to five days a week'], [5, 'Six or seven days a week']]
AGREE = [[i, str(i)] for i in range(1, 8)] + [[C.CANNOT_JUDGE, 'Cannot judge']]


def scale(label, lo, hi, n=7):
    return models.IntegerField(
        label=label, choices=[[i, str(i)] for i in range(1, n + 1)],
        widget=widgets.RadioSelectHorizontal,
        help_text=f'1 = {lo}, {n} = {hi}' if lo else '')


def fam(cat):
    return models.IntegerField(
        label=cat, choices=[[1, '1 Not at all'], [2, '2'], [3, '3'], [4, '4'], [5, '5 Extremely']],
        widget=widgets.RadioSelectHorizontal)


def agree(label):
    return models.IntegerField(label=label, choices=AGREE, widget=widgets.RadioSelectHorizontal)


def active(player):
    pp = player.participant
    return pp.consented and not pp.excluded


# ---------------------------------------------------------------- models
class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    if subsession.round_number != 1:
        return
    session = subsession.session
    session.blocks = {'low': [], 'high': []}
    session.block_counts = {'low': 0, 'high': 0}
    master = random.Random()
    for p in subsession.get_players():
        pp = p.participant
        pp.seed = master.randint(1, 10**9)
        pp.battery = task_bank.build_battery(pp.seed)
        pp.arm = ''
        pp.consented = True
        pp.excluded = False


def assign_arm(player):
    """Blocks of four within prior AI use (PS2): less than weekly vs weekly+."""
    session = player.session
    stratum = 'low' if player.ps2 <= 2 else 'high'
    blocks, counts = session.blocks, session.block_counts
    if not blocks[stratum]:
        new_block = list(C.ARMS)
        random.shuffle(new_block)
        blocks[stratum] = new_block
        counts[stratum] += 1
    arm = blocks[stratum].pop()
    session.blocks, session.block_counts = blocks, counts  # save
    player.participant.arm = arm
    player.arm = arm
    player.randomization_block = f"{stratum}-{counts[stratum]}"


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    arm = models.StringField(blank=True)
    randomization_block = models.StringField(blank=True)

    # --- consent
    consent = models.BooleanField(
        label='Do you agree to take part in this study?',
        choices=[[True, 'Yes, I agree'], [False, 'No, I do not want to take part']],
        widget=widgets.RadioSelect)

    # --- background (before assignment)
    age_group = models.StringField(
        label='What is your age group?',
        choices=['18-20', '21-24', '25-29', '30+', 'Prefer not to say'])
    study_year = models.StringField(
        label='What is your year of study?',
        choices=['First', 'Second', 'Third', 'Fourth', 'Graduate', 'Other'])
    major = models.StringField(label='What is your major?')
    ps1 = models.IntegerField(
        label='How familiar are you with AI chat tools such as ChatGPT, Gemini, or Claude?',
        choices=[[1, 'Not at all'], [2, 'Slightly'], [3, 'Moderately'], [4, 'Very'], [5, 'Extremely']],
        widget=widgets.RadioSelect)
    ps2 = models.IntegerField(label='During the past month, how often did you use an AI chat tool?',
                              choices=FREQ, widget=widgets.RadioSelect)
    ps3 = models.IntegerField(label='During the past month, how often did you use AI to find or compare products?',
                              choices=FREQ, widget=widgets.RadioSelect)
    ps4 = models.IntegerField(
        label='How would you rate your ability to get useful results from AI chat tools?',
        choices=[[1, '1 Very low'], [2, '2'], [3, '3'], [4, '4'], [5, '5 Very high']],
        widget=widgets.RadioSelectHorizontal)
    search_freq = models.IntegerField(
        label='During the past month, how often did you use a search engine to find or compare products?',
        choices=FREQ, widget=widgets.RadioSelect)
    shop_freq = models.StringField(
        label='During the past three months, how often did you buy something online?',
        choices=['Never', 'Less than monthly', 'One to three times a month', 'About weekly',
                 'Several times a week'],
        widget=widgets.RadioSelect)
    fam_mouse = fam('Wireless mouse')
    fam_kettle = fam('Electric kettle')
    fam_headphones = fam('Wireless headphones')
    fam_backpack = fam('Laptop backpack')
    fam_vacuum = fam('Cordless vacuum')
    fam_speaker = fam('Portable speaker')
    attention_check = models.StringField(
        label='For this item, please select "Sometimes."',
        choices=['Never', 'Rarely', 'Sometimes', 'Often', 'Very often'],
        widget=widgets.RadioSelectHorizontal)
    attention_passed = models.BooleanField()

    # --- AI limitations knowledge (0-3, "Not sure" = incorrect)
    know1 = models.StringField(label='"AI chat tools can state incorrect facts confidently."',
                               choices=['True', 'False', 'Not sure'], widget=widgets.RadioSelect)
    know2 = models.StringField(
        label="Which source is generally best for checking a product's current listed price?",
        choices=['Retailer product page', 'AI answer without a source', 'Social-media post', 'Not sure'],
        widget=widgets.RadioSelect)
    know3 = models.StringField(
        label='"A product review or rating count given by an AI chat tool is always current."',
        choices=['True', 'False', 'Not sure'], widget=widgets.RadioSelect)
    ai_limitations_knowledge = models.IntegerField()

    # --- comprehension (answers overwritten each attempt; full log kept)
    comp_q1 = models.StringField(label='Must the selected product meet all requirements or only some?',
                                 choices=['All requirements', 'Only some requirements', 'At least half'],
                                 widget=widgets.RadioSelect)
    comp_q2 = models.StringField(label='Can you use tools other than those assigned to you?',
                                 choices=['Yes', 'No'], widget=widgets.RadioSelect)
    comp_q3 = models.StringField(label='Must you buy the product?', choices=['Yes', 'No'],
                                 widget=widgets.RadioSelect)
    comp_q4 = models.StringField(label='What should you do if you cannot find a product?',
                                 choices=['Enter the closest product I found',
                                          'Choose "I could not find one"',
                                          'Leave the page until time runs out'],
                                 widget=widgets.RadioSelect)
    comp_q5 = models.StringField(label='Which tools are you allowed to use to find products?',
                                 choices=[C.ARM_LABELS[a] for a in C.ARMS] + ['Any website or tool I want'],
                                 widget=widgets.RadioSelect)
    comp_attempts = models.IntegerField(initial=0)
    comp_passed = models.BooleanField(initial=False)
    comp_log = models.LongStringField(initial='')

    # --- task record (one per round)
    is_practice = models.BooleanField()
    task_order = models.IntegerField()      # 0 = practice, 1..6 scored
    task_id = models.StringField()
    template_id = models.StringField()
    difficulty = models.StringField()
    task_params = models.LongStringField()
    start_ts = models.FloatField()
    deadline_ts = models.FloatField()
    end_ts = models.FloatField()
    time_sec = models.FloatField()
    submitted = models.BooleanField(initial=False)
    no_answer = models.BooleanField(initial=False)
    timed_out = models.BooleanField(initial=False)
    draft_json = models.LongStringField(initial='')
    first_action_sec = models.FloatField()
    n_launcher_queries = models.IntegerField(initial=0)
    n_chatgpt_opens = models.IntegerField(initial=0)
    focus_lost = models.IntegerField(initial=0)

    # --- answer form (participant-reported claims, verified later)
    result_choice = models.StringField(blank=True)
    ans_product = models.StringField(blank=True, label='Brand and product / model name')
    ans_variant = models.StringField(blank=True, label='Selected size / color / variant (if any)')
    ans_retailer = models.StringField(blank=True, label='Retailer (e.g., Amazon, Walmart, Best Buy)')
    ans_seller = models.StringField(blank=True, label='Marketplace seller (if different from retailer)')
    ans_url = models.LongStringField(blank=True, label='Direct product-page link (URL)')
    ans_price = models.FloatField(blank=True, label='Price in USD')
    ans_price_nv = models.BooleanField(blank=True, widget=widgets.CheckboxInput, label='Could not verify')
    ans_rating = models.FloatField(blank=True, min=0, max=5, label='Star rating (out of 5)')
    ans_rating_nv = models.BooleanField(blank=True, widget=widgets.CheckboxInput, label='Could not verify')
    ans_count = models.IntegerField(blank=True, min=0, label='Number of customer ratings')
    ans_count_nv = models.BooleanField(blank=True, widget=widgets.CheckboxInput, label='Could not verify')
    ans_stock = models.StringField(blank=True, label='Availability',
                                   choices=['In stock', 'Not in stock / preorder / backorder',
                                            'Could not verify'])
    ans_attribute = models.StringField(blank=True, label='Value for the extra requirement')
    ans_attribute_nv = models.BooleanField(blank=True, widget=widgets.CheckboxInput, label='Could not verify')

    # --- ratings after each scored task
    confidence = scale('How confident are you that your selected product meets every requirement?',
                       'Not at all confident', 'Completely confident')
    difficulty_rating = scale('How difficult was this task?', 'Very easy', 'Very hard')
    effort_rating = scale('How much mental effort did this task require?', 'Very little', 'Very much')

    # --- post-survey
    post_easy = agree('The assigned tools made it easy to find a product meeting the requirements.')
    post_trust = agree('I trusted the product information provided by the assigned tools.')
    post_reuse = agree('I would use these tools again for this type of product search.')
    post_ads = agree('The results seemed influenced by advertising or paid placement.')
    post_fast = agree('The assigned tools helped me finish quickly.')
    wl_mental = scale('Overall, how mentally demanding were the tasks?', 'Very low', 'Very high')
    wl_effort = scale('Overall, how much effort did the tasks require?', 'Very low', 'Very high')
    wl_frustration = scale('Overall, how frustrated did you feel?', 'Very low', 'Very high')
    open_easy_hard = models.LongStringField(blank=True, label='What made the tasks easy or difficult?')
    open_confusing = models.LongStringField(blank=True, label='Was anything confusing or missing?')
    b_tool_mainly = models.StringField(
        label='Did you mainly use search, mainly use AI, or use both about equally?',
        choices=['Mainly search', 'Mainly AI (ChatGPT)', 'Both about equally'], widget=widgets.RadioSelect)


class Event(ExtraModel):
    """Log of in-oTree actions: launcher searches, ChatGPT opens, focus loss, drafts."""
    player = models.Link(Player)
    ts = models.FloatField()
    sec_into_task = models.FloatField()
    kind = models.StringField()
    detail = models.LongStringField()


def custom_export(players):
    yield ['participant_code', 'arm', 'round', 'task_id', 'ts', 'sec_into_task', 'kind', 'detail']
    for e in Event.filter():
        p = e.player
        yield [p.participant.code, p.participant.arm, p.round_number, p.task_id,
               e.ts, e.sec_into_task, e.kind, e.detail]


def task_for_round(player):
    if player.round_number == 1:
        return task_bank.PRACTICE_TASK
    return player.participant.battery[player.round_number - 2]


# ---------------------------------------------------------------- pages
class Consent(Page):
    form_model = 'player'
    form_fields = ['consent']

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.consented = player.consent


class Background(Page):
    form_model = 'player'
    form_fields = ['age_group', 'study_year', 'major', 'ps1', 'ps2', 'ps3', 'ps4',
                   'search_freq', 'shop_freq', 'fam_mouse', 'fam_kettle', 'fam_headphones',
                   'fam_backpack', 'fam_vacuum', 'fam_speaker', 'attention_check']

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1 and active(player)

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.attention_passed = player.attention_check == 'Sometimes'


class Knowledge(Page):
    form_model = 'player'
    form_fields = ['know1', 'know2', 'know3']

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1 and active(player)

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.ai_limitations_knowledge = sum([
            player.know1 == 'True', player.know2 == 'Retailer product page', player.know3 == 'False'])
        assign_arm(player)  # randomize after baseline items


class Instructions(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1 and active(player)

    @staticmethod
    def vars_for_template(player):
        arm = player.participant.arm
        return dict(arm=arm, arm_label=C.ARM_LABELS[arm], minutes=player.session.config['task_seconds'] // 60)


COMP_EXPLAIN = {
    'comp_q1': 'The product must meet ALL listed requirements.',
    'comp_q2': 'No. Use only the tools assigned to your group.',
    'comp_q3': 'No. You do not buy anything.',
    'comp_q4': 'Choose "I could not find one."',
    'comp_q5': 'Use only the tools listed in the instructions for your group.',
}


def comp_correct(player):
    return {
        'comp_q1': 'All requirements', 'comp_q2': 'No', 'comp_q3': 'No',
        'comp_q4': 'Choose "I could not find one"',
        'comp_q5': C.ARM_LABELS[player.participant.arm],
    }


def comp_wrong(player):
    correct = comp_correct(player)
    return [f for f in correct if getattr(player, f) != correct[f]]


class Comprehension1(Page):
    """Attempt 1. Attempt 2 shows feedback; attempt 3 adds a standard clarification."""
    template_name = 'ai_search/Comprehension.html'
    form_model = 'player'
    form_fields = ['comp_q1', 'comp_q2', 'comp_q3', 'comp_q4', 'comp_q5']
    attempt = 1

    @classmethod
    def is_displayed(cls, player):
        return (player.round_number == 1 and active(player)
                and not player.comp_passed and player.comp_attempts == cls.attempt - 1)

    @classmethod
    def vars_for_template(cls, player):
        feedback = []
        if cls.attempt > 1:
            feedback = [COMP_EXPLAIN[f] for f in comp_wrong(player)]
        return dict(attempt=cls.attempt, feedback=feedback, clarify=cls.attempt == 3,
                    arm_label=C.ARM_LABELS[player.participant.arm], arm=player.participant.arm)

    @classmethod
    def before_next_page(cls, player, timeout_happened):
        player.comp_attempts = cls.attempt
        wrong = comp_wrong(player)
        player.comp_passed = not wrong
        log = json.loads(player.comp_log or '[]')
        log.append({'attempt': cls.attempt, 'wrong': wrong})
        player.comp_log = json.dumps(log)
        if wrong and cls.attempt == 3:
            player.participant.excluded = True  # do not start scored tasks


class Comprehension2(Comprehension1):
    attempt = 2


class Comprehension3(Comprehension1):
    attempt = 3


class TaskIntro(Page):
    @staticmethod
    def is_displayed(player):
        return active(player)

    @staticmethod
    def vars_for_template(player):
        return dict(is_practice=player.round_number == 1, n=player.round_number - 1,
                    n_total=task_bank.N_SCORED_TASKS)

    @staticmethod
    def before_next_page(player, timeout_happened):
        t = task_for_round(player)
        player.arm = player.participant.arm
        player.is_practice = player.round_number == 1
        player.task_order = player.round_number - 1
        player.task_id = t['task_id']
        player.template_id = t['template_id']
        player.difficulty = t['difficulty']
        player.task_params = json.dumps(t)
        secs = player.session.config['practice_seconds' if player.is_practice else 'task_seconds']
        player.start_ts = time.time()
        player.deadline_ts = player.start_ts + secs


class Task(Page):
    form_model = 'player'
    timer_text = 'Time left for this task:'

    @staticmethod
    def is_displayed(player):
        return active(player)

    @staticmethod
    def get_form_fields(player):
        f = ['result_choice', 'ans_product', 'ans_variant', 'ans_retailer', 'ans_seller', 'ans_url',
             'ans_price', 'ans_price_nv', 'ans_rating', 'ans_rating_nv', 'ans_count', 'ans_count_nv',
             'ans_stock']
        if task_for_round(player).get('attribute'):
            f += ['ans_attribute', 'ans_attribute_nv']
        return f

    @staticmethod
    def get_timeout_seconds(player):
        return player.deadline_ts - time.time()  # same deadline after refresh

    @staticmethod
    def vars_for_template(player):
        t = task_for_round(player)
        arm = player.participant.arm
        return dict(task=t, requirements=task_bank.requirements_list(t), arm=arm,
                    arm_label=C.ARM_LABELS[arm], is_practice=player.round_number == 1,
                    n=player.round_number - 1, n_total=task_bank.N_SCORED_TASKS,
                    has_attr=bool(t.get('attribute')),
                    show_search=arm in ('S', 'D', 'B'), show_ai=arm in ('A', 'B'),
                    search_label='Google (Web filter)' if arm in ('S', 'B') else 'Google')

    @staticmethod
    def js_vars(player):
        arm = player.participant.arm
        return dict(search_url=C.GOOGLE_DEFAULT if arm == 'D' else C.GOOGLE_WEB,
                    ai_url=player.session.config['ai_url'],
                    draft=json.loads(player.draft_json or '{}'))

    @staticmethod
    def live_method(player, data):
        now = time.time()
        if player.field_maybe_none('end_ts') or now > player.deadline_ts:
            return
        kind = data.get('kind', '')
        detail = data.get('detail', '')
        if kind == 'draft':
            player.draft_json = json.dumps(detail)[:20000]
            return  # drafts are not logged as events
        if kind not in ('search', 'open_chatgpt', 'focus_lost', 'focus_back'):
            return
        if kind in ('search', 'open_chatgpt') and player.field_maybe_none('first_action_sec') is None:
            player.first_action_sec = now - player.start_ts
        if kind == 'search':
            if player.participant.arm == 'A':
                return  # not permitted for AI-only
            player.n_launcher_queries += 1
        elif kind == 'open_chatgpt':
            if player.participant.arm in ('S', 'D'):
                return  # not permitted for search groups
            player.n_chatgpt_opens += 1
        elif kind == 'focus_lost':
            player.focus_lost += 1
        Event.create(player=player, ts=now, sec_into_task=now - player.start_ts,
                     kind=kind, detail=str(detail)[:2000])

    @staticmethod
    def error_message(player, values):
        if values['result_choice'] == 'no_answer':
            return
        if values['result_choice'] != 'submitted':
            return 'Please use one of the two buttons at the bottom.'
        errs = {}
        for f in ['ans_product', 'ans_retailer', 'ans_url']:
            if not (values.get(f) or '').strip():
                errs[f] = 'Please fill this in.'
        for f in ['ans_price', 'ans_rating', 'ans_count', 'ans_attribute']:
            if f in values and values[f] in (None, '') and not values.get(f + '_nv'):
                errs[f] = 'Enter a value or tick "Could not verify".'
        if not values.get('ans_stock'):
            errs['ans_stock'] = 'Please choose one.'
        return errs or None

    @staticmethod
    def before_next_page(player, timeout_happened):
        now = time.time()
        player.end_ts = now
        late = now > player.deadline_ts + 3  # small network grace
        if timeout_happened or late:
            player.timed_out = True  # draft kept for audit, not a submitted answer
        elif player.result_choice == 'no_answer':
            player.no_answer = True
        else:
            player.submitted = True
        player.time_sec = round(min(now, player.deadline_ts) - player.start_ts, 1)
        Event.create(player=player, ts=now, sec_into_task=now - player.start_ts,
                     kind='end', detail='timeout' if player.timed_out else player.result_choice)


class PracticeDone(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1 and active(player)


class TaskRating(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player):
        return player.round_number > 1 and active(player)

    @staticmethod
    def get_form_fields(player):
        f = ['difficulty_rating', 'effort_rating']
        return (['confidence'] + f) if player.submitted else f


class PostSurvey(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS and active(player)

    @staticmethod
    def get_form_fields(player):
        f = ['post_easy', 'post_trust', 'post_reuse', 'post_ads', 'post_fast',
             'wl_mental', 'wl_effort', 'wl_frustration']
        if player.participant.arm == 'B':
            f.append('b_tool_mainly')
        return f + ['open_easy_hard', 'open_confusing']


class Completion(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player):
        cfg = player.session.config
        return dict(consented=player.participant.consented, excluded=player.participant.excluded,
                    base=f"{cfg['participation_fee']:.2f}", bonus=f"{cfg['bonus_per_correct']:.2f}",
                    max_total=f"{cfg['max_total_pay']:.2f}", code=player.participant.code)


page_sequence = [
    Consent, Background, Knowledge, Instructions,
    Comprehension1, Comprehension2, Comprehension3,
    TaskIntro, Task, PracticeDone, TaskRating,
    PostSurvey, Completion,
]
