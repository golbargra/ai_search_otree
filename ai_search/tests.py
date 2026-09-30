import random
from otree.api import Bot, Submission, SubmissionMustFail, expect
from . import *


class PlayerBot(Bot):
    def play_round(self):
        r = self.round_number
        arm_bad = False
        if r == 1:
            yield Consent, dict(consent=True)
            yield Background, dict(
                age_group='21-24', study_year='Third', major='Econ', ps1=3,
                ps2=random.choice([1, 2, 3, 4, 5]), ps3=2, ps4=3, search_freq=3,
                shop_freq='About weekly', fam_mouse=3, fam_kettle=2, fam_headphones=4,
                fam_backpack=3, fam_vacuum=1, fam_speaker=2, attention_check='Sometimes')
            yield Knowledge, dict(know1='True', know2='Retailer product page', know3='Not sure')
            expect(self.player.ai_limitations_knowledge, 2)
            yield Instructions
            ok = dict(comp_q1='All requirements', comp_q2='No', comp_q3='No',
                      comp_q4='Choose "I could not find one"',
                      comp_q5=C.ARM_LABELS[self.participant.arm])
            # first attempt wrong, second right
            yield Comprehension1, dict(ok, comp_q3='Yes')
            yield Comprehension2, ok
            expect(self.player.comp_passed, True)
        yield TaskIntro
        yield SubmissionMustFail(Task, dict(result_choice='submitted', ans_product='x'))
        if r % 2:
            yield Submission(Task, dict(
                result_choice='submitted', ans_product='Logitech M185', ans_retailer='Amazon',
                ans_url='https://example.com/p', ans_price=19.99, ans_rating_nv=True,
                ans_count=1200, ans_stock='In stock', ans_attribute='yes'), check_html=False)
            expect(self.player.submitted, True)
        else:
            yield Submission(Task, dict(result_choice='no_answer'))
            expect(self.player.no_answer, True)
        if r == 1:
            yield PracticeDone
        else:
            if self.player.submitted:
                yield TaskRating, dict(confidence=5, difficulty_rating=3, effort_rating=4)
            else:
                yield TaskRating, dict(difficulty_rating=3, effort_rating=4)
        if r == C.NUM_ROUNDS:
            d = dict(post_easy=5, post_trust=-1, post_reuse=6, post_ads=3, post_fast=5,
                     wl_mental=4, wl_effort=4, wl_frustration=2)
            if self.participant.arm == 'B':
                d['b_tool_mainly'] = 'Both about equally'
            yield PostSurvey, d


def call_live_method(method, **kwargs):
    method(1, {'kind': 'search', 'detail': 'wireless mouse under 35'})
    method(1, {'kind': 'open_chatgpt', 'detail': ''})
    method(1, {'kind': 'focus_lost', 'detail': ''})
    method(1, {'kind': 'draft', 'detail': {'ans_product': 'draft x'}})
