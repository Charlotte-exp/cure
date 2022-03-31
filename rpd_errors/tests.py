from otree.api import Currency as c, currency_range, expect, Bot
from . import *

import random


class PlayerBot(Bot):
    def play_round(self):
        if self.round_number <= self.participant.last_round:
            yield Decision, dict(observed_decision=random.choice([0, 1]))

        yield Results

        if self.round_number == self.participant.last_round:
            yield End
            yield StrategyBox, {"strategy_box": 'n/a'}
            yield CommentBox, {"comment_box": 'n/a'}
            yield Payment
            yield ProlificLink
