from ._builtin import Page, WaitPage
from .models import Constants

# Each page that a player sees is defined in this file
# Each class in this file represents a page

# Each page can inherit either a "Page" class or a "WaitPage" class
# If a page inherits a "WaitPage" class, the page is simply a page to wait until
# all players arrive
# Example 1: class BeginWaitPage(Waitpage) is a page class that inherits "WaitPage" class
# This page is not shown to players and is used to wait until all players are on the same page (no pun intended!)

# Example 2: class SellerChoice(Page) is a page that inherits "Page" class
# This page is shown to players

# For detailed documentation regarding pages, please refer to oTree's documentation page below
# https://otree.readthedocs.io/en/latest/pages.html

def get_private_range_string(seller_private_range_midpoint):
    return "%d-%d" % (seller_private_range_midpoint - 1, seller_private_range_midpoint + 1)

# This is a transition page that is not shown to the end-user
class BeginWaitPage(WaitPage):
    # This method is called once all players arrive at this page.
    def after_all_players_arrive(self):
        # init_round() is a method defined in models.py
        # The init_round() method does two things as described below
        # 1. It generates an estimated asset value between 1-20
        # 2. It determines the true asset value based on the estimated value from Step 1
        # 3. It sets initial budgets for all sellers and buyers
        self.group.init_round()


class SellerChoiceNotEnoughBudget(Page):
    def is_displayed(self):
        return self.player.role() == 'seller' and self.player.budget < Constants.more_precise_reporting_cost

    def vars_for_template(self):
        seller_private_range_midpoints_by_player_id = {
            1: self.group.seller1_private_range_midpoint,
            2: self.group.seller2_private_range_midpoint,
            3: self.group.seller3_private_range_midpoint
        }

        seller_private_range = get_private_range_string(seller_private_range_midpoints_by_player_id[self.player.id_in_group])

        return {
            'seller_private_range': seller_private_range
        }


class SellerChoiceLowHigh(Page):
    form_model = 'group'

    def is_displayed(self):
        return self.player.role() == 'seller' and self.player.budget >= Constants.more_precise_reporting_cost

    # Return reporting precision level form field based on player id
    def get_form_fields(self):
        form_fields_by_player_id = {
            1: ['seller1_did_report_more_precise'],
            2: ['seller2_did_report_more_precise'],
            3: ['seller3_did_report_more_precise']
        }

        return form_fields_by_player_id[self.player.id_in_group]

    def vars_for_template(self):
        seller_private_range_midpoints_by_player_id = {
            1: self.group.seller1_private_range_midpoint,
            2: self.group.seller2_private_range_midpoint,
            3: self.group.seller3_private_range_midpoint
        }

        seller_private_range = get_private_range_string(seller_private_range_midpoints_by_player_id[self.player.id_in_group])

        return {
            'seller_private_range': seller_private_range
        }

    def before_next_page(self):
        if self.player.role() == 'seller':
            self.player.update_seller_budget_after_reporting()


class SellerChoiceReportingRange(Page):
    form_model = 'group'

    def is_displayed(self):
        return self.player.role() == 'seller'

    # Return reported ranges form field based on player id
    def get_form_fields(self):
        form_fields_by_player_id = {
            1: ['seller1_reported_range'],
            2: ['seller2_reported_range'],
            3: ['seller3_reported_range']
        }

        return form_fields_by_player_id[self.player.id_in_group]

    def vars_for_template(self):
        seller_private_range_midpoints_by_player_id = {
            1: self.group.seller1_private_range_midpoint,
            2: self.group.seller2_private_range_midpoint,
            3: self.group.seller3_private_range_midpoint
        }

        did_seller_report_more_precise_by_id = {
            1: self.group.seller1_did_report_more_precise,
            2: self.group.seller2_did_report_more_precise,
            3: self.group.seller3_did_report_more_precise
        }

        seller_private_range = get_private_range_string(seller_private_range_midpoints_by_player_id[self.player.id_in_group])
        did_seller_report_more_precise = did_seller_report_more_precise_by_id[self.player.id_in_group]

        return {
            'seller_private_range': seller_private_range,
            'did_seller_report_more_precise': did_seller_report_more_precise
        }

    def before_next_page(self):
        pass


# This is a transition page that is not shown to the end-user
# By the time all players arrive on this page, sellers have finished
# picking reporting options and reported ranges
# Seller grade calculation should be done in this step
class SellerChoiceResultWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_seller_grades()


class BuyerChoice(Page):
    form_model = 'player'

    # Input text fields to be shown to buyers
    form_fields = ['bid_asset1', 'bid_asset2', 'bid_asset3']

    def get_seller_history(self, player_id):
        rounds = range(2, Constants.num_practice_rounds + 1) if self.round_number <= Constants.num_practice_rounds else range(Constants.num_practice_rounds + 1, Constnats.num_rounds + 1)

        return list(rounds)

    # is_displayed() is used to show this page only to the buyers
    def is_displayed(self):
        return self.player.role() == 'buyer'

    def vars_for_template(self):
        sellers_info = [
                {
                    'id': 1,
                    'reported_range': self.group.seller1_reported_range,
                    'grade': self.group.seller1_grade,
                    'history': self.get_seller_history(1),
                },
                {
                    'id': 2,
                    'reported_range': self.group.seller2_reported_range,
                    'grade': self.group.seller2_grade,
                    'history': self.get_seller_history(2),
                },
                {
                    'id': 3,
                    'reported_range': self.group.seller3_reported_range,
                    'grade': self.group.seller3_grade,
                    'history': self.get_seller_history(3),
                },
            ]

        return {
            'sellers': sellers_info
        }

    def error_message(self, values):
        if values["bid_asset1"] + values["bid_asset2"] + values["bid_asset3"] > self.player.budget:
            return 'Sum of the bids exceeds your budget.'


# This is a transition page that is not shown to the end-user
# Bid winners and payoffs for each round are determined here
class RoundResultWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.determine_bid_winners()
        self.group.set_payoffs()


class RoundResult(Page):
    def vars_for_template(self):
        buyers = self.group.get_buyers()

        return {
            # This array of objects is used in the Results page
            # to display range of high asset probabilities, true asset value,
            # other buyers' bids, and winners

            'assets': [
                {
                    'id': 1,
                    'reported_range': self.group.seller1_reported_range,
                    'true_value': self.group.asset1_true_value,
                    'seller_grade': self.group.seller1_grade,
                    'winning_bid': self.group.asset1_max_bid,
                    'bids': list(map(lambda b: {
                        'player_id': b.id_in_group,
                        'amount': b.bid_asset1,
                        'did_win': b.did_win_asset1,
                        'is_self': b.id_in_group == self.player.id_in_group
                    }, buyers))
                },
                {
                    'id': 2,
                    'reported_range': self.group.seller2_reported_range,
                    'true_value': self.group.asset2_true_value,
                    'seller_grade': self.group.seller2_grade,
                    'winning_bid': self.group.asset2_max_bid,
                    'bids': list(map(lambda b: {
                        'player_id': b.id_in_group,
                        'amount': b.bid_asset2,
                        'did_win': b.did_win_asset2,
                        'is_self': b.id_in_group == self.player.id_in_group
                    }, buyers))
                },
                {
                    'id': 3,
                    'reported_range': self.group.seller3_reported_range,
                    'true_value': self.group.asset3_true_value,
                    'seller_grade': self.group.seller3_grade,
                    'winning_bid': self.group.asset3_max_bid,
                    'bids': list(map(lambda b: {
                        'player_id': b.id_in_group,
                        'amount': b.bid_asset3,
                        'did_win': b.did_win_asset3,
                        'is_self': b.id_in_group == self.player.id_in_group
                    }, buyers))
                },
            ],
        }


class PracticeOutro(Page):
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_practice_rounds


page_sequence = [
    BeginWaitPage,
    SellerChoiceNotEnoughBudget,
    SellerChoiceLowHigh,
    SellerChoiceReportingRange,
    SellerChoiceResultWaitPage,
    BuyerChoice,
    RoundResultWaitPage,
    RoundResult,
    PracticeOutro
]
