from otree.api import Currency as c, currency_range, expect, Bot
from . import *


class PlayerBot(Bot):
    def play_round(self):
        if self.round_number == 1:
            yield Consent
            # yield Welcome
            yield Instructions, {"q1": '2', "q2": '4', "q3": '2' }




        #     if self.round_number == 1:
        #         yield pages.Consent
        #         yield pages.Welcome, {"q1": '2', "q2": '3'}
        #         if self.participant.vars['subgroup'] == 'high':
        #             yield pages.Instructions1, {"q3a": '3', "q4": '2', "q5": '2'}
        #             yield pages.Instructions2, {"q6h": '1', "q7h": '3', "q8h": '2'}
        #         else:
        #             if self.participant.vars['subgroup'] == 'low':
        #                 yield pages.Instructions1, {"q3b": '3', "q4": '2', "q5": '2'}
        #                 yield pages.Instructions2, {"q6l": '1', "q7l": '3', "q8l": '2'}
