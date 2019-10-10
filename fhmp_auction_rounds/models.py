import random
import numpy as np
from numpy.random import choice

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c
)

author = 'Your name here'

doc = """
Practice rounds
"""


class Constants(BaseConstants):
    name_in_url = 'fhmp_practice_rounds'
    players_per_group = None

    # Practice = 2 rounds
    # Main = 20 rounds
    # num_rounds should be # practice rounds + # main rounds
    num_rounds = 4

    # Currency definitions
    buyer_initial_endowment_practice_rounds = c(40)
    seller_initial_endowment_practice_rounds = c(5)

    buyer_initial_endowment_main_rounds = c(100)
    seller_initial_endowment_main_rounds = c(5)

    high_detail_disclosure_cost = c(2)

    # Generate disclose intervals dict
    disclose_intervals = {}

    low_range = 5
    high_range = 3

    for min_value in range(1, 20 - low_range + 2):
        max_value = min_value + low_range - 1
        key = str(min_value) + '-' + str(max_value)

        disclose_intervals[key] = {
            'label': 'Low ' + key,
            'min': min_value,
            'max': max_value
        }

    for min_value in range(1, 20 - high_range + 2):
        max_value = min_value + high_range - 1
        key = str(min_value) + '-' + str(max_value)

        disclose_intervals[key] = {
            'label': 'High ' + key,
            'min': min_value,
            'max': max_value
        }

    # Create a list of strings to be displayed in form fields
    # shown to users
    disclose_interval_choices = list(
        map(lambda x: [x[0], x[1]['label']], disclose_intervals.items()))

    # Choices for disclose levels
    reporting_option_choices = [
        [False, 'Less Precise (5 numbers wide) (No cost)'],
        [True, 'More Precise (3 numbers wide) (Cost: 2 points)'],
    ]


class Subsession(BaseSubsession):
    def creating_session(self):
        print('creating_session')


class Group(BaseGroup):
    print('running Group init')

    # These boolean fields indicate whether the user has selected high level of disclosure
    asset1_disclose_high = models.BooleanField(
        choices=Constants.reporting_option_choices,
        widget=widgets.RadioSelect,
        initial=False
    )

    asset2_disclose_high = models.BooleanField(
        choices=Constants.reporting_option_choices,
        widget=widgets.RadioSelect,
        initial=False
    )

    asset3_disclose_high = models.BooleanField(
        choices=Constants.reporting_option_choices,
        widget=widgets.RadioSelect,
        initial=False
    )

    # Disclose intervals
    asset1_disclose_interval = models.StringField(
        choices=Constants.disclose_interval_choices,
        widget=widgets.RadioSelect,
        blank=False
    )

    asset2_disclose_interval = models.StringField(
        choices=Constants.disclose_interval_choices,
        widget=widgets.RadioSelect,
        blank=False
    )

    asset3_disclose_interval = models.StringField(
        choices=Constants.disclose_interval_choices,
        widget=widgets.RadioSelect,
        blank=False,
        initial=list(Constants.disclose_intervals.keys())[0]
    )

    # Assets' true values based on each probability
    asset1_true_value = models.CurrencyField()
    asset2_true_value = models.CurrencyField()
    asset3_true_value = models.CurrencyField()

    # Since there is a fixed number of assets, each asset's probability and disclose_interval should be listed here
    asset1_est_value = models.CurrencyField(min=1, max=20)
    asset2_est_value = models.CurrencyField(min=1, max=20)
    asset3_est_value = models.CurrencyField(min=1, max=20)

    asset1_fact_checker_midpoint = models.IntegerField(min=1, max=20)
    asset2_fact_checker_midpoint = models.IntegerField(min=1, max=20)
    asset3_fact_checker_midpoint = models.IntegerField(min=1, max=20)

    seller1_grade = models.StringField()
    seller2_grade = models.StringField()
    seller3_grade = models.StringField()

    asset1_max_bid = models.CurrencyField()
    asset2_max_bid = models.CurrencyField()
    asset3_max_bid = models.CurrencyField()

    # A simple getter for the cost of high reporting option
    # Since there is no way to access the value of Constants.high_detail_disclosure_cost
    # from pages.py, this method is used to proxy the value
    def get_high_detail_disclosure_cost(self):
        return Constants.high_detail_disclosure_cost

    # Generate estimated/true values
    def init_round(self):
        # High asset probabilities
        self.asset1_est_value = c(random.randint(1, 20))
        self.asset2_est_value = c(random.randint(1, 20))
        self.asset3_est_value = c(random.randint(1, 20))

        # Asset true values
        self.asset1_true_value = self.draw_asset_true_value(
            self.asset1_est_value)
        self.asset2_true_value = self.draw_asset_true_value(
            self.asset2_est_value)
        self.asset3_true_value = self.draw_asset_true_value(
            self.asset3_est_value)

        is_start_of_practice_rounds = self.round_number == 1
        is_start_of_main_rounds = self.round_number == 3

        for p in self.get_players():
            if is_start_of_practice_rounds:
                if p.role() == 'seller':
                    p.budget = Constants.seller_initial_endowment_practice_rounds
                else:
                    p.budget = Constants.buyer_initial_endowment_practice_rounds

            elif is_start_of_main_rounds:
                if p.role() == 'seller':
                    p.budget = Constants.seller_initial_endowment_main_rounds
                else:
                    p.budget = Constants.buyer_initial_endowment_main_rounds

            else:
                p.budget = p.in_round(self.round_number - 1).budget

    # A static method to draw a fact checker range given an estimated value
    @staticmethod
    def draw_fact_checker_range_midpoint(est_value):
        weights = [1, 2, 3, 2, 1]
        possible_midpoints = [est_value - 2, est_value -
                              1, est_value, est_value + 1, est_value + 2]

        for i in range(5):
            midpoint = possible_midpoints[i]

            if midpoint - 2 <= 0 or midpoint + 2 > 20:
                weights[i] = 0

        # Normalize weights array to sum to 1
        # If the array is not normalized, numpy's choice() method will throw an error
        weights = weights / np.sum(weights)

        return int(choice(possible_midpoints, p=weights))

    # A static method to get a true asset value given an estimated value
    # 30% prob chance that true == estimated
    # 18% prob chance for true == estimated + 1 or true == estimated - 1
    # Remaining probabilities are equally split
    @staticmethod
    def draw_asset_true_value(est_value):
        # Convert estimated value to int since est_value is a Currency type
        est_value_int = int(est_value)

        # Possible true value range is [1, 2, ..., 19, 20]
        possible_values = [_ for _ in range(1, 21)]

        # When estimated value is 1
        if est_value_int == 1:
            weights = [((1 - 0.3 - 0.18) / 18) for _ in range(20)]
            weights[est_value_int - 1] = 0.3
            weights[1] = 0.18

        # When estimated value is 20
        elif est_value_int == 20:
            weights = [((1 - 0.3 - 0.18) / 18) for _ in range(20)]
            weights[est_value_int - 1] = 0.3
            weights[18] = 0.18

        # When estimated value is between 2 and 19
        else:
            weights = [0.02 for _ in range(20)]
            weights[est_value_int - 1] = 0.3
            weights[est_value_int - 2] = 0.18
            weights[est_value_int] = 0.18

        # Use numpy's random.choice() to pick a random value from a list
        # with probabilities list
        # and convert the value back to currency
        return c(float(choice(possible_values, p=weights)))

    # Get sellers
    def get_sellers(self):
        # A list to hold IDs of all buyers
        sellers = []

        # Loop through all players
        for p in self.get_players():
            # Check if seller
            if p.role() == 'seller':
                # Collect ids of all sellers
                sellers.append(p)

        return sellers

    # Get buyers
    def get_buyers(self):
        # A list to hold IDs of all buyers
        buyers = []

        # Loop through all players
        for p in self.get_players():
            # Check if buyer
            if p.role() == 'buyer':
                # Collect ids of all buyers
                buyers.append(p)

        return buyers

    # Get buyer ids
    def get_buyer_ids(self):
        return list(map(lambda b: b.id_in_group, self.get_buyers()))

    # Set fact checker mipdoints for each asset
    # The fact checker ranges are drawn from the possible ranges
    def set_fact_checker_midpoints(self):
        self.asset1_fact_checker_midpoint = self.draw_fact_checker_range_midpoint(
            self.asset1_est_value)

        self.asset2_fact_checker_midpoint = self.draw_fact_checker_range_midpoint(
            self.asset2_est_value)

        self.asset3_fact_checker_midpoint = self.draw_fact_checker_range_midpoint(
            self.asset3_est_value)

    # Set seller grades based on differences between estimated/disclosed asset values
    # This method should be called from a WaitPage after sellers select reporting options
    def set_seller_grades(self):
        # Need to draw fact checker ranges and set midpoints first
        self.set_fact_checker_midpoints()

        self.seller1_grade = self.calculate_seller_grade(
            int(Constants.disclose_intervals[self.asset1_disclose_interval]['min'] + (Constants.disclose_intervals[self.asset1_disclose_interval]['max'] - Constants.disclose_intervals[self.asset1_disclose_interval]['min']) / 2), int(self.asset1_fact_checker_midpoint))

        self.seller2_grade = self.calculate_seller_grade(
            int(Constants.disclose_intervals[self.asset2_disclose_interval]['min'] + (Constants.disclose_intervals[self.asset2_disclose_interval]['max'] - Constants.disclose_intervals[self.asset2_disclose_interval]['min']) / 2), int(self.asset2_fact_checker_midpoint))

        self.seller3_grade = self.calculate_seller_grade(
            int(Constants.disclose_intervals[self.asset3_disclose_interval]['min'] + (Constants.disclose_intervals[self.asset3_disclose_interval]['max'] - Constants.disclose_intervals[self.asset3_disclose_interval]['min']) / 2), int(self.asset3_fact_checker_midpoint))

    # A: if the midpoint of the reported range is equal to, + 1 or - 1 of the midpoint of the fact checker’s range
    # B: if the midpoint of the reported range is + or - 2 or 3 from the midpoint of the fact checker’s range
    # C: if the midpoint of the reported range is + or – 4 from the midpoint of the fact checker’s range
    # F: everything else
    @staticmethod
    def calculate_seller_grade(reported_range_midpoint, fact_checker_range_midpoint):
        midpoint_diff = abs(reported_range_midpoint -
                            fact_checker_range_midpoint)

        if midpoint_diff <= 1:
            return 'A'
        elif midpoint_diff <= 3:
            return 'B'
        elif midpoint_diff <= 4:
            return 'C'
        else:
            return 'F'

    def get_seller_grade(self, seller_id):
        grade_dict = {
            1: self.seller1_grade,
            2: self.seller2_grade,
            3: self.seller3_grade
        }

        return grade_dict[seller_id]

    # Determine bid winners
    def determine_bid_winners(self):
        group = self

        # A list to hold IDs of all buyers
        buyer_ids = map(lambda p: p.id_in_group, self.get_buyers())

        # Lists of bids for each asset by all buyers
        asset1_bids = []
        asset2_bids = []
        asset3_bids = []

        # Lists of max bids for each asset (in case tie happens)
        asset1_max_bidders = []
        asset2_max_bidders = []
        asset3_max_bidders = []

        # Loop through all players
        for p in group.get_buyers():
            # Add bids on each asset to corresponding lists
            asset1_bids.append(p.bid_asset1)
            asset2_bids.append(p.bid_asset2)
            asset3_bids.append(p.bid_asset3)

        # Get max bid on each asset
        self.asset1_max_bid = max(asset1_bids)
        self.asset2_max_bid = max(asset2_bids)
        self.asset3_max_bid = max(asset3_bids)

        # Find max bidders (this is to break ties)
        for buyer_id in buyer_ids:
            p = group.get_player_by_id(buyer_id)

            if p.bid_asset1 >= self.asset1_max_bid:
                asset1_max_bidders.append(buyer_id)

            if p.bid_asset2 >= self.asset2_max_bid:
                asset2_max_bidders.append(buyer_id)

            if p.bid_asset3 >= self.asset3_max_bid:
                asset3_max_bidders.append(buyer_id)

        # Randomly select a winner amongst highest bidders for each asset
        group.get_player_by_id(random.choice(
            asset1_max_bidders)).did_win_asset1 = True
        group.get_player_by_id(random.choice(
            asset2_max_bidders)).did_win_asset2 = True
        group.get_player_by_id(random.choice(
            asset3_max_bidders)).did_win_asset3 = True

    # Set payoffs of all players
    def set_payoffs(self):
        for p in self.get_players():
            p.set_payoff()

    # Get the true value of a seller's asset
    def get_asset_true_value(self, seller_id):
        true_value = {
            1: self.asset1_true_value,
            2: self.asset2_true_value,
            3: self.asset3_true_value
        }

        return true_value[seller_id]

    # Get max bids for an asset by asset's seller id
    def get_asset_max_bid(self, seller_id):
        assets = {
            1: self.asset1_max_bid,
            2: self.asset2_max_bid,
            3: self.asset3_max_bid
        }

        return assets[seller_id]

    # Get the reporting cost of a seller
    def get_seller_disclosure_cost(self, seller_id):
        seller_disclose_high = {
            1: self.asset1_disclose_high,
            2: self.asset2_disclose_high,
            3: self.asset3_disclose_high
        }

        return Constants.high_detail_disclosure_cost if seller_disclose_high[seller_id] else 0


class Player(BasePlayer):
    # Buyer budget for all rounds
    # For practice rounds, buyer budget is 40 (2 rounds * initial endowment)
    # For main rounds, buyer budget is  (20 rounds * initial endowment)
    budget = models.CurrencyField(min=0, blank=False)

    # For buyers
    # Bids on assets
    bid_asset1 = models.CurrencyField(min=0, max=20, initial=0, blank=False)
    bid_asset2 = models.CurrencyField(min=0, max=20, initial=0, blank=False)
    bid_asset3 = models.CurrencyField(min=0, max=20, initial=0, blank=False)

    # For buyers
    # Bids results
    did_win_asset1 = models.BooleanField(initial=False)
    did_win_asset2 = models.BooleanField(initial=False)
    did_win_asset3 = models.BooleanField(initial=False)

    round_earning = models.CurrencyField(min=0, initial=0)

    # Returns 'seller' or 'buyer'
    def role(self):
        return self.participant.vars['role']

    # Update budget after the seller chooses a reporting option
    def update_seller_budget_after_reporting(self):
        self.budget -= self.group.get_seller_disclosure_cost(self.id_in_group)

    # Calculate earning and add to payoffs
    # This method is run at the end of each round
    def set_payoff(self):
        # Seller earning from round
        if self.role() == 'seller':
            seller_asset_max_bid = self.group.get_asset_max_bid(
                self.id_in_group)

            self.round_earning = seller_asset_max_bid

        # Buyer payoffs
        elif self.role() == 'buyer':
            if self.did_win_asset1:
                self.round_earning += self.group.asset1_true_value - self.bid_asset1

            if self.did_win_asset2:
                self.round_earning += self.group.asset2_true_value - self.bid_asset2

            if self.did_win_asset3:
                self.round_earning += self.group.asset3_true_value - self.bid_asset3

        self.payoff += self.round_earning
        self.budget += self.round_earning
