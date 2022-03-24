from otree.api import *


doc = """
        Your app description
        """

import random

class C(BaseConstants):
    NAME_IN_URL = 'rpd_errors'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 50

    """ variables for randomish end round, used in the intro app at the mo"""
    min_rounds = 1
    proba_next_round = 0.50

    conversion = '20pts = £0.05'

    """
    Matrix format payoffs
    temptation = betray, sucker = betrayed, reward = both cooperate, punishment = both defect 
    """
    temptation = cu(50)
    sucker = cu(12)
    reward = cu(26)
    punishment = cu(25)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    last_round = models.IntegerField()
    left_hanging = models.CurrencyField()

    decision = models.IntegerField(
            choices=[
                [1, '1'],
                [0, '2'],
            ],
            doc="""This player's decision""",
            widget=widgets.RadioSelect
        )


### FUNCTIONS
def get_random_number_of_rounds(self):
    """
    Creating the random-ish number of rounds a group plays for. PP plays for at least 20 rounds (set on constants),
    then they have a 50% chance of another round, and then again 50% chance of another round.
    This function creates a last round number following this method.
    """
    number_of_rounds = C.min_rounds
    while C.proba_next_round > random.random():
        number_of_rounds += 1
    return number_of_rounds


def group_by_arrival_time_method(subsession, waiting_players):
    players = [p for p in waiting_players]
    if len(waiting_players) >= 2:
        players = [players[0], players[1]]
        last_round = subsession.get_random_number_of_rounds()
        for p in players:
            p.participant.last_round = last_round
            p.last_round = p.participant.last_round
        return players


def other_player(player: Player):
    return player.get_others_in_group()[0]


def get_payoff(player: Player):
    payoff_matrix = {
        1:
            {
                1: C.reward,
                0: C.sucker
            },
        0:
            {
                1: C.temptation,
                0: C.punishment
            }
    }
    player.payoff = payoff_matrix[player.decision][player.other_player.decision]


def set_payoffs(group: Group):
    for p in group.get_players():
        get_payoff(p)


# PAGES
class PairingWaitPage(WaitPage):
    """
    The Waitroom. This wait page has two purposes: making sure pps don't wait too long for other players in case there
    is little traffic, and allows one pp to leave before being grouped with others so that a dropout at the instruction
    level does not mean all pp in the group are out.
    The code below keeps the groups the same across all rounds automatically.
    We added a special pairing method in models.py.
    The waitroom has a 5min timer after which the pp is given a code to head back to prolific.
    This is coded on the template below and uses a javascript. (don't forget to paste the correct link!)
    """
    group_by_arrival_time = True

    def is_displayed(player: Player):
        return player.round_number == 1

    template_name = 'rpd_errors/Waitroom.html'


class Decision(Page):
    """
    This is where the pp are presented with the PD options and give their decision. It's simple form fields from Django.
    There is a timer to check for dropouts. If one of the players' timer runs out the others are linked back to prolific
    """
    form_model = 'player'
    form_fields = ['decision']

    def is_displayed(player: Player):
        """
        This page is displayed only if the player is neither left hanging (1) nor a dropout (2).
        And only for the number of rounds assigned to the group by the random number function.
        """
        if player.left_hanging == 1 or player.left_hanging == 2:
            return False
        elif player.round_number <= player.participant.last_round:
            return True

    timer_text = 'If you stay inactive for too long you will be considered a dropout:'
    timeout_seconds = 2 * 60

    def before_next_page(player, timeout_happened):
        """
        Dropout check code! If the timer set above runs out, all the other players in the group become left_hanging = 1
        and are jumped to the leftHanging page with a link to Prolific. The dropout also goes to that page but gets
        a different text (left_hanging = 2).
        Decisions for the missed round are automatically filled to avoid an NONE type error.
        """
        me = player
        co_player = me.other_player
        if timeout_happened:
            co_player.left_hanging = 1
            me.left_hanging = 2
            me.decision = 1

    def vars_for_template(player: Player):
        """
        This function is for displaying variables in the HTML file using Django.
        The variables are inserted into calculation or specifications and given a display name used in the HTML.
        """
        me = player
        co_player = me.other_player
        if player.round_number > 1:
            return {
                'round_number': player.round_number,
                'co_player_previous_decision': co_player.in_round(player.round_number - 1).decision,
                'previous_decision': me.in_round(player.round_number - 1).decision,
            }
        else:
            return {
                'round_number': player.round_number,
            }


class ResultsWaitPage(WaitPage):
    """
    This wait page is necessary to compile the payoffs as the results can only be displayed on the results page if all
    the players have made a decision. Thus players have to wait for the decision of the others before moving on to the
    results page.
    I use a template for some special text rather than just the body_text variable.
    """

    after_all_players_arrive = set_payoffs
    template_name = 'control_PD/ResultsWaitPage.html'

    def is_displayed(player: Player):
        """
        This page is displayed only if the number of rounds assigned to the group by the random number function.
        Curiously it does not need to be hidden for left_hanging participants...
        """
        if player.round_number <= player.participant.last_round:
            return True


class Results(Page):
    """
    This page is for the round results. It gives feedback on what the co_players decided for this round.
    It has a timer so that a dropout is automatically pushed to the decision page where the dropout function is.
    """

    def is_displayed(player: Player):
        """
        This page is displayed only if the player is neither left hanging (1) or a dropout (2).
        And only for the number of rounds assigned to the group by the random number function.
        """
        if player.left_hanging == 1 or player.left_hanging == 2:
            return False
        elif player.round_number <= player.participant.last_round:
            return True
    timer_text = 'You are about to be automatically moved to the next results summary page'
    timeout_seconds = 2 * 60

    def vars_for_template(player: Player):
        """
        This function is for displaying variables in the HTML file using Django.
        The variables are inserted into calculation or specifications and given a display name used in the HTML.
        """
        me = player
        co_player = me.other_player
        return {
            'my_decision': me.decision,
            'co_player_decision': co_player.decision,
            'my_payoff': me.payoff,
        }


class Previous(Page):
    """
    This page is a reminder of what happened in the previous round.
    It has a timer so that a dropout is automatically pushed to the decision page where the dropout function is.
    """

    def is_displayed(player: Player):
        """
        This page is displayed only if the player is neither left hanging (1) or a dropout (2).
        And only for the number of rounds assigned to the group by the random number function.
        """
        if player.left_hanging == 1 or player.left_hanging == 2:
            return False
        elif player.round_number <= player.participant.last_round:
            return True

    timer_text = 'You are about to be automatically moved to the next round decision page'
    timeout_seconds = 1 * 60

    def vars_for_template(player: Player):
        """
        This function is for displaying variables in the HTML file using Django.
        The variables are inserted into calculation or specifications and given a display name used in the HTML.
        """
        me = player
        co_player = me.other_player
        return {
            'my_decision': me.decision,
            'co_player_decision': co_player.decision,
            'my_payoff': me.payoff,
        }


class End(Page):
    """
    This page is for final combined round results. It displays the payoffs of each round played for all co_players
    and sums the total across round of the player.
    """

    def is_displayed(player: Player):
        """
        This page is displayed only if the player is neither left hanging (1) or a dropout (2).
        And only appears on the last round.
        """
        if player.left_hanging == 1 or player.left_hanging == 2:
            return False
        elif player.round_number == participant.last_round:
            return True

    def vars_for_template(player: Player):
        """
        This function is for displaying variables in the HTML file using Django.
        The variables are inserted into calculation or specifications and given a display name used in the HTML.
        """
        me = player
        co_player = player.other_player
        return {
            'player_in_all_rounds': me.in_all_rounds(),
            'co_player_in_all_rounds': co_player.in_all_rounds(),
            'total_payoff': sum([p.payoff for p in me.in_all_rounds()]),
        }


class Demographics(Page):
    """ This page displays survey box to record pp's demographics. it's just made of simple form fields. """
    form_model = 'player'
    form_fields = ['age', 'gender', 'income', 'education', 'ethnicity']

    def is_displayed(player: Player):
        """
        This page is displayed only if the player is neither left hanging (1) or a dropout (2).
        And only appears on the last round.
        """
        if player.left_hanging == 1 or player.left_hanging == 2:
            return False
        elif player.round_number == player.participant.last_round:
            return True


class CommentBox(Page):
    form_model = 'player'
    form_fields = ['comment_box']

    def is_displayed(player: Player):
        """ This function makes the page appear only on the last random-ish round """
        if player.left_hanging == 1 or player.left_hanging == 2:
            return False
        elif player.round_number == player.participant.last_round:
            return True


class Payment(Page):
    """
    This page is for final payment in GBP. A lot of the mechanics relating to payment is set in the settings
    (currency/point exchange rate, currency). It displays the total for each game and the total combined, the show-up fee,
    the conversion rate, the total bonus in GBP and the final payment in GBP of bonus and participation fee combined.
    """

    def is_displayed(player: Player):
        """
        This page is displayed only if the player is neither left hanging (1) or a dropout (2).
        And only appears on the last round.
        """
        if player.left_hanging == 1 or player.left_hanging == 2:
            return False
        elif player.round_number == player.participant.last_round:
            return True

    def vars_for_template(player: Player):
        """"
        The currency per point and participation fee are set in settings.py. However it can only be set in GBP per point
        which is not human friendly. So I need to reverse it for display.
        The bonus and final payment are not saved in the data sheet automatically.
        I'd have to save the result in a form field under the player class I guess... but it is annoying.
        Since I use the oTree variable "payoff" it all gets displayed in the admin interface and I can download that.
        """
        participant = player.participant
        session = player.session
        return {
            'total_payoff': participant.payoff,
            'currency_per_points': session.config['real_world_currency_per_point'],
            'participation_fee': session.config['participation_fee'],
            'bonus': participant.payoff.to_real_world_currency(session),
            'final_payment': participant.payoff_plus_participation_fee()
        }


class LeftHanging(Page):
    """
    This page is for dropouts. If a participant quits after the waitroom there is a timer on the results
    and decision page that redirect them to this page. Here depending on who left and who was left hanging,
    they get a different message (based on their left_hanging value).
    The left-hanging pp get a link to go back to Prolific (don't forget to paste the correct link!).
    """

    def is_displayed(player: Player):
        """ This page is displayed only if the player is either left hanging (1) or a dropout (2)."""
        if player.left_hanging == 1 or player.left_hanging == 2:
            return True


class ProlificLink(Page):
    """
    This page redirects pp to prolific automatically with a javascript (don't forget to put paste the correct link!).
    There is a short text and the link in case it is not automatic.
    """

    def is_displayed(player: Player):
        """ This page only appears on the last round. It's after LeftHanging so no need to hide it from dropouts."""
        return player.round_number == player.participant.last_round


page_sequence = [
    PairingWaitPage,
    Decision,
    ResultsWaitPage,
    Results,
    # Previous,
    End,
    # Demographics,
    # CommentBox,
    Payment,
    LeftHanging,
    ProlificLink,
]
