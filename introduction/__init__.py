from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'introduction'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class Consent(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'participation_fee': self.session.config['participation_fee'],
        }


class Welcome(Page):
    form_model = 'player'
    form_fields = ['q1', 'q2']

    def is_displayed(self):
        return self.round_number == 1

    def error_message(self, values):
        if values['q1'] != 2:
            return 'Answer to question 1 is incorrect. Check the instructions again and give a new answer'
        if values['q2'] != 3:
            return 'Answer to question 2 is incorrect. Check the instructions again and give a new answer'


class Instructions1(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == 1

    def get_form_fields(self):
        """ make one q3 for each subgroup that displays only to each to avoid empty field errors"""
        if self.participant.vars['subgroup'] == 'high':
            return ['q3a', 'q4', 'q5']
        else:
            return ['q3b', 'q4', 'q5']

    def error_message(self, values):
        if self.participant.vars['subgroup'] == 'high':
            if values['q3a'] != 3:
                return 'Answer to question 1 is incorrect. Check the instructions again and give a new answer'
        if self.participant.vars['subgroup'] == 'low':
            if values['q3b'] != 3:
                return 'Answer to question 1 is incorrect. Check the instructions again and give a new answer'
        if values['q4'] != 2:
            return 'Answer to question 2 is incorrect. Check the instructions again and give a new answer'
        if values['q5'] != 2:
            return 'Answer to question 3 is incorrect. Check the instructions again and give a new answer'

    def vars_for_template(self):
        return{
            'my_treatment': self.participant.vars['subgroup'],

            'initial_endowment_high': Constants.endowment_high * Constants.min_rounds,
            'initial_endowment_low': Constants.endowment_low * Constants.min_rounds,
        }


class Instructions2(Page):
    form_model = 'player'

    def get_form_fields(self):
        """ make one q3 for each subgroup that displays only to each to avoid empty field errors"""
        if self.participant.vars['subgroup'] == 'high':
            return ['q6h', 'q7h', 'q8h']
        else:
            return ['q6l', 'q7l', 'q8l']

    def is_displayed(self):
        return self.round_number == 1

    def error_message(self, values):
        if self.participant.vars['subgroup'] == 'high':
            if values['q6h'] != 1:
                return 'Answer to question 1 is incorrect. Check the instructions again and give a new answer'
            if values['q7h'] != 3:
                return 'Answer to question 2 is incorrect. Check the instructions again and give a new answer'
            if values['q8h'] != 2:
                return 'Answer to question 3 is incorrect. Check the instructions again and give a new answer'
        if self.participant.vars['subgroup'] == 'low':
            if values['q6l'] != 1:
                return 'Answer to question 1 is incorrect. Check the instructions again and give a new answer'
            if values['q7l'] != 3:
                return 'Answer to question 2 is incorrect. Check the instructions again and give a new answer'
            if values['q8l'] != 2:
                return 'Answer to question 3 is incorrect. Check the instructions again and give a new answer'

    def vars_for_template(self):
        return{
            'my_treatment': self.participant.vars['subgroup'],

            'cost_high': Constants.c_high,
            'cost_low': Constants.c_low,
            'benefit_high': Constants.b_high,
            'benefit_low': Constants.b_low,

            'sucker_high': -Constants.c_high,
            'temptation_high': Constants.b_high,
            'reward_high': Constants.b_high - Constants.c_high,

            'sucker_low': -Constants.c_low,
            'temptation_low': Constants.b_low,
            'reward_low': Constants.b_low - Constants.c_low,
        }


page_sequence = [
    Consent,
    # Welcome,
    # Instructions1,
    # Instructions2,
]