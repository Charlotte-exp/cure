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

    min_rounds = 20
    proba_next_round = 0.50
    max_bonus = cu(5)

    error_rate = 0.10

    session_time = 12

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

    condition = models.StringField()
    num_failed_attempts = models.IntegerField(initial=0)

    q1 = models.IntegerField(
            choices=[
                [1, '0 other participants'],
                [2, '1 other participant'],
                [3, f'2 other participants']
            ],
            verbose_name='With how many participants will you be paired with in this study?',
            widget=widgets.RadioSelect
        )

    q2 = models.IntegerField(
            choices=[
                [1, f'{C.sucker}'],
                [2, f'{C.punishment}'],
                [3, f'{C.reward}'],
                [4, f'{C.temptation}']
            ],
            verbose_name='What is your payoff if you defect but the other player cooperates?',
            widget=widgets.RadioSelect
        )

    q3 = models.IntegerField(
            choices=[
                [1, '10%'],
                [2, '50%'],
                [3, '100%']
            ],
            verbose_name=f'What are the chances that '
                         f'there will be another round after the {C.min_rounds}th round?',
            widget=widgets.RadioSelect
        )


# Functions

def creating_session(subsession):
    """
    AWe use itertools to assign treatment regularly to make sure there is a somewhat equal amount of each in the
    session but also that is it equally distributed in the sample. (So pp don't have to wait to long get matched
    in a pair. It simply cycles through the list of treatments (high & low) and that's saved in the participant vars.
    """
    treatments = itertools.cycle(['no_errors', 'with_errors'])
    for p in subsession.get_players():
        p.condition = next(treatments)
        p.participant.condition = p.condition
        # print('condition is', p.condition)
        # print('vars condition is', p.participant.condition)


# PAGES
class Consent(Page):
    def is_displayed(player: Player):
        return player.round_number == 1

    def vars_for_template(player: Player):
        return {
            'participation_fee': player.session.config['participation_fee'],
        }


class Welcome(Page):

    def is_displayed(player: Player):
        return player.round_number == 1


class Instructions(Page):
    form_model = 'player'
    form_fields = ['q1', 'q2', 'q3']

    def is_displayed(player: Player):
        return player.round_number == 1

    def vars_for_template(player: Player):
        """"
        The currency per point and participation fee are set in settings.py.
        """
        return {
            'currency_per_points': player.session.config['real_world_currency_per_point'],
            'error_rate': math.ceil(C.error_rate * 100),
            'delta': math.ceil(C.proba_next_round * 100),
        }

    @staticmethod
    def error_message(player: Player, values):
        """
        records the number of time the page was submitted with an error. which specific error is not recorded.
        """
        solutions = dict(q1=2, q2=4, q3=2)
        # error_message can return a dict whose keys are field names and whose values are error messages
        errors = {f: 'This answer is wrong' for f in solutions if values[f] != solutions[f]}
        # print('errors is', errors)
        if errors:
            player.num_failed_attempts += 1
            return errors


page_sequence = [
    Consent,
    # Welcome,
    Instructions,
]