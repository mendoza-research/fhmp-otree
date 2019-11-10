import random
import numpy as np
from numpy.random import choice

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c
)

author = 'Kimberly Mendoza'

doc = """
Models for auction rounds
"""
# Set the number of practice/main rounds here
num_practice_rounds = 4
num_main_rounds = 20

class Constants(BaseConstants):
    name_in_url = 'fhmp_practice_rounds'
    players_per_group = None

    # Define the number of rounds class variables
    num_practice_rounds=num_practice_rounds
    num_main_rounds=num_main_rounds

    # number of total rounds (practice + main)
    num_rounds = num_practice_rounds + num_main_rounds

    # Currency definitions
    buyer_initial_endowment_practice_rounds = c(200)
    seller_initial_endowment_practice_rounds = c(20)

    buyer_initial_endowment_main_rounds = c(200)
    seller_initial_endowment_main_rounds = c(20)

    more_precise_reporting_cost = c(2)

    # Generate reporting ranges dict
    reporting_ranges = {}

    # The ranges must be odd numbers
    low_range = 5
    high_range = 3

    for min_value in range(1, 20 - low_range + 2):
        max_value = min_value + low_range - 1
        key = str(min_value) + '-' + str(max_value)

        reporting_ranges[key] = {
            'label': 'Low ' + key,
            'min': min_value,
            'max': max_value
        }

    for min_value in range(1, 20 - high_range + 2):
        max_value = min_value + high_range - 1
        key = str(min_value) + '-' + str(max_value)

        reporting_ranges[key] = {
            'label': 'High ' + key,
            'min': min_value,
            'max': max_value
        }

    # Create a list of strings to be displayed in form fields
    # shown to users
    reporting_range_choices = list(
        map(lambda x: [x[0], x[1]['label']], reporting_ranges.items()))

    # Choices for reporting precision
    reporting_precision_choices = [
        [False, 'Less Precise (5 numbers wide) (No cost)'],
        [True, 'More Precise (3 numbers wide) (Cost: 2 points)'],
    ]


class Subsession(BaseSubsession):
    def creating_session(self):
        # print('creating_session')
        pass


class Group(BaseGroup):
    # These boolean fields indicate whether the user has selected more precise reporting option
    seller1_did_report_more_precise = models.BooleanField(
        choices=Constants.reporting_precision_choices,
        widget=widgets.RadioSelect,
        initial=False
    )

    seller2_did_report_more_precise = models.BooleanField(
        choices=Constants.reporting_precision_choices,
        widget=widgets.RadioSelect,
        initial=False
    )

    seller3_did_report_more_precise = models.BooleanField(
        choices=Constants.reporting_precision_choices,
        widget=widgets.RadioSelect,
        initial=False
    )

    # Reported ranges
    seller1_reported_range = models.StringField(
        choices=Constants.reporting_range_choices,
        widget=widgets.RadioSelect,
        blank=False
    )

    seller2_reported_range = models.StringField(
        choices=Constants.reporting_range_choices,
        widget=widgets.RadioSelect,
        blank=False
    )

    seller3_reported_range = models.StringField(
        choices=Constants.reporting_range_choices,
        widget=widgets.RadioSelect,
        blank=False,
        initial=list(Constants.reporting_ranges.keys())[0]
    )

    # Assets' true values based on each probability
    asset1_true_value = models.CurrencyField()
    asset2_true_value = models.CurrencyField()
    asset3_true_value = models.CurrencyField()

    seller1_private_range_midpoint = models.CurrencyField(min=2, max=19)
    seller2_private_range_midpoint = models.CurrencyField(min=2, max=19)
    seller3_private_range_midpoint = models.CurrencyField(min=2, max=19)

    asset1_fact_checker_midpoint = models.IntegerField(min=1, max=20)
    asset2_fact_checker_midpoint = models.IntegerField(min=1, max=20)
    asset3_fact_checker_midpoint = models.IntegerField(min=1, max=20)

    seller1_grade = models.StringField()
    seller2_grade = models.StringField()
    seller3_grade = models.StringField()

    asset1_max_bid = models.CurrencyField()
    asset2_max_bid = models.CurrencyField()
    asset3_max_bid = models.CurrencyField()

    # Generate estimated/true values
    def init_round(self):
        # High asset probabilities
        self.seller1_private_range_midpoint = c(random.randint(2, 19))
        self.seller2_private_range_midpoint = c(random.randint(2, 19))
        self.seller3_private_range_midpoint = c(random.randint(2, 19))

        # Asset true values
        self.asset1_true_value = self.draw_asset_true_value(
            self.seller1_private_range_midpoint)
        self.asset2_true_value = self.draw_asset_true_value(
            self.seller2_private_range_midpoint)
        self.asset3_true_value = self.draw_asset_true_value(
            self.seller3_private_range_midpoint)

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
    def draw_fact_checker_range_midpoint(private_range_midpoint):
        weights = [1, 2, 3, 2, 1]
        possible_fact_checker_midpoints = [private_range_midpoint - 2, private_range_midpoint -
                              1, private_range_midpoint, private_range_midpoint + 1, private_range_midpoint + 2]

        for i in range(5):
            midpoint = possible_fact_checker_midpoints[i]

            if midpoint - 2 <= 0 or midpoint + 2 > 20:
                weights[i] = 0

        # Normalize weights array to sum to 1
        # If the array is not normalized, numpy's choice() method will throw an error
        weights = weights / np.sum(weights)

        return int(choice(possible_fact_checker_midpoints, p=weights))

    # A static method to get a true asset value given an estimated value
    # 30% prob chance that true == estimated
    # 18% prob chance for true == estimated + 1 or true == estimated - 1
    # Remaining probabilities are equally split
    @staticmethod
    def draw_asset_true_value(private_range_midpoint):
        # Convert estimated value to int since private_range_midpoint is a Currency type
        private_range_midpoint_int = int(private_range_midpoint)

        # Possible true value range is [1, 2, ..., 19, 20]
        possible_values = [_ for _ in range(1, 21)]

        weights = [0.01 for _ in range(20)]
        weights[private_range_midpoint_int - 2] = 0.2
        weights[private_range_midpoint_int - 1] = 0.43
        weights[private_range_midpoint_int] = 0.2

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
            self.seller1_private_range_midpoint)

        self.asset2_fact_checker_midpoint = self.draw_fact_checker_range_midpoint(
            self.seller2_private_range_midpoint)

        self.asset3_fact_checker_midpoint = self.draw_fact_checker_range_midpoint(
            self.seller3_private_range_midpoint)

    # Set seller grades based on differences between private range/fact checker range
    # This method should be called from a WaitPage after sellers select reporting options
    def set_seller_grades(self):
        # Need to draw fact checker ranges and set midpoints first
        self.set_fact_checker_midpoints()

        self.seller1_grade = self.calculate_seller_grade(
            int(Constants.reporting_ranges[self.seller1_reported_range]['min'] + (Constants.reporting_ranges[self.seller1_reported_range]['max'] - Constants.reporting_ranges[self.seller1_reported_range]['min']) / 2), int(self.asset1_fact_checker_midpoint))

        self.seller2_grade = self.calculate_seller_grade(
            int(Constants.reporting_ranges[self.seller2_reported_range]['min'] + (Constants.reporting_ranges[self.seller2_reported_range]['max'] - Constants.reporting_ranges[self.seller2_reported_range]['min']) / 2), int(self.asset2_fact_checker_midpoint))

        self.seller3_grade = self.calculate_seller_grade(
            int(Constants.reporting_ranges[self.seller3_reported_range]['min'] + (Constants.reporting_ranges[self.seller3_reported_range]['max'] - Constants.reporting_ranges[self.seller3_reported_range]['min']) / 2), int(self.asset3_fact_checker_midpoint))

    # Pass: if the midpoint of the reported range is equal to, + 1 or - 1 of the midpoint of the fact checker’s range
    # Pass: if the midpoint of the reported range is + or - 2 or 3 from the midpoint of the fact checker’s range
    # Pass: if the midpoint of the reported range is + or – 4 from the midpoint of the fact checker’s range
    # Fail: everything else
    @staticmethod
    def calculate_seller_grade(reported_range_midpoint, fact_checker_range_midpoint):
        midpoint_diff = abs(reported_range_midpoint -
                            fact_checker_range_midpoint)

        if midpoint_diff <= 1:
            return 'Pass'
        elif midpoint_diff <= 3:
            return 'Pass'
        elif midpoint_diff <= 4:
            return 'Pass'
        else:
            return 'Fail'

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

    def get_seller_history(self, player_id):
        previous_rounds = range(1, self.round_number) if self.round_number <= Constants.num_practice_rounds else range(Constants.num_practice_rounds + 1, self.round_number)

        history = [] 

        for round_number in previous_rounds:
            group = self.in_round(round_number)

            seller_reported_ranges_by_id = {
                1: group.seller1_reported_range,
                2: group.seller2_reported_range,
                3: group.seller3_reported_range
            }


            seller_grade_by_id = {
                1: group.seller1_grade, 
                2: group.seller2_grade, 
                3: group.seller3_grade
            }

            asset_true_value_by_id = {
                1: group.asset1_true_value, 
                2: group.asset2_true_value, 
                3: group.asset3_true_value
            }

            history.append({
                'round_number': round_number if round_number <= Constants.num_practice_rounds else round_number - Constants.num_practice_rounds, 
                'reported_range': seller_reported_ranges_by_id[player_id], 
                'precision': 'More precise' if seller_did_report_more_precise_by_id[player_id] else 'Less precise',
                'seller_grade': seller_grade_by_id[player_id],
                'asset_true_value': asset_true_value_by_id[player_id]
            })

        return history

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
        self.budget -= self.group.get_seller_reporting_cost(self.id_in_group)

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
