from otree.api import *

import itertools
import math

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'introduction'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    min_rounds = 1
    proba_next_round = 0.50

    session_time = 15
    conversion = '20pts = £0.05'

    """
    Matrix format payoffs
    temptation = betray, sucker = betrayed, reward = both cooperate, punishment = both defect 
    """
    temptation = cu(0.25)
    sucker = cu(0)
    reward = cu(0.15)
    punishment = cu(0.05)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    errors = models.StringField()


# Functions

def creating_session(subsession):
    """
    AWe use itertools to assign treatment regularly to make sure there is a somewhat equal amount of each in the
    session but also that is it equally distributed in the sample. (So pp don't have to wait to long get matched
    in a pair. It simply cycles through the list of treatments (high & low) and that's saved in the participant vars.
    """
    treatments = itertools.cycle(['0%', '5%'])
    for p in subsession.get_players():
        p.errors = next(treatments)
        p.participant.errors = p.errors
        # print('errors is', p.errors)
        # print('vars errors is', p.participant.errors)


# PAGES
class Consent(Page):
    def is_displayed(player: Player):
        return player.round_number == 1

    def vars_for_template(player: Player):
        return {
            'participation_fee': player.session.config['participation_fee'],
        }


class Welcome(Page):
    form_model = 'player'
    form_fields = ['q1', 'q2']

    def is_displayed(player: Player):
        return player.round_number == 1

    def error_message(player, values):
        if values['q1'] != 2:
            return 'Answer to question 1 is incorrect. Check the instructions again and give a new answer'
        if values['q2'] != 3:
            return 'Answer to question 2 is incorrect. Check the instructions again and give a new answer'


class Instructions(Page):
    form_model = 'player'

    def is_displayed(player: Player):
        return player.round_number == 1

    def vars_for_template(player: Player):
        """"
        The currency per point and participation fee are set in settings.py.
        """
        return {
            'currency_per_points': player.session.config['real_world_currency_per_point'],
            'delta': math.ceil(C.proba_next_round * 100)
        }


page_sequence = [
    Consent,
    # Welcome,
    Instructions,
]