import random
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
	num_rounds = 2
	# Currency definitions
	buyer_initial_endowment = c(20) * num_rounds
	seller_initial_endowment = c(5)
	high_detail_disclosure_cost = c(2)

	# Generate disclose intervals dict
	disclose_intervals = {}

	low_range = 4
	high_range = 2

	for min_value in range(1, 20 - low_range + 1):
		key = str(min_value) + '-' + str(min_value + low_range)

		disclose_intervals[key] = {
			'label': 'Low ' + key,
			'min': min_value,
			'max': min_value + low_range
		}

	for min_value in range(1, 20 - high_range + 1):
		key = str(min_value) + '-' + str(min_value + high_range)

		disclose_intervals[key] = {
			'label': 'High ' + key,
			'min': min_value,
			'max': min_value + high_range
		}

	# Create a list of strings to be displayed in form fields
	# shown to users
	disclose_interval_choices = list(map(lambda x: [x[0], x[1]['label']], disclose_intervals.items()))

	# Choices for disclose levels
	reporting_option_choices = [
		[False, 'Low (No cost)'],
		[True, 'High (2 points)'],
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
		self.asset1_true_value = self.draw_asset_true_value(self.asset1_est_value)
		self.asset2_true_value = self.draw_asset_true_value(self.asset2_est_value)
		self.asset3_true_value = self.draw_asset_true_value(self.asset3_est_value)

		for p in self.get_players():
			if p.role() == 'seller':
				p.budget = Constants.seller_initial_endowment
			else:
				p.budget = Constants.buyer_initial_endowment

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

	# Set seller grades based on differences between estimated/disclosed asset values
	# This method should be called from a WaitPage after sellers select reporting options
	def set_seller_grades(self):
		self.seller1_grade = self.calculate_seller_grade(
			Constants.disclose_intervals[self.asset1_disclose_interval]['min'],
			Constants.disclose_intervals[self.asset1_disclose_interval]['max'],
			self.asset1_est_value
		)

		self.seller2_grade = self.calculate_seller_grade(
			Constants.disclose_intervals[self.asset2_disclose_interval]['min'],
			Constants.disclose_intervals[self.asset2_disclose_interval]['max'],
			self.asset2_est_value
		)

		self.seller3_grade = self.calculate_seller_grade(
			Constants.disclose_intervals[self.asset3_disclose_interval]['min'],
			Constants.disclose_intervals[self.asset3_disclose_interval]['max'],
			self.asset3_est_value
		)

	# A: in range
	# B: within 1 outside the range
	# C: within 2 outside the range
	# D: within 3 outside the range
	# F: within 4 or more outside the range
	@staticmethod
	def calculate_seller_grade(disclose_min, disclose_max, est_value):
		# Describes the padding added to left and right to the
		# reported asset range
		# Change the values below to adjust how seller grades are determined
		# Note that the condition D > C > B > A must be met
		grade_a_padding = 0
		grade_b_padding = 1
		grade_c_padding = 2
		grade_d_padding = 3

		if disclose_min - grade_a_padding <= est_value <= disclose_max + grade_a_padding:
			return 'A'
		elif disclose_min - grade_b_padding <= est_value <= disclose_max + grade_b_padding:
			return 'B'
		elif disclose_min - grade_c_padding <= est_value <= disclose_max + grade_c_padding:
			return 'C'
		elif disclose_min - grade_d_padding <= est_value <= disclose_max + grade_d_padding:
			return 'D'
		else:
			# Anything else
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
		group.get_player_by_id(random.choice(asset1_max_bidders)).did_win_asset1 = True
		group.get_player_by_id(random.choice(asset2_max_bidders)).did_win_asset2 = True
		group.get_player_by_id(random.choice(asset3_max_bidders)).did_win_asset3 = True

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
			seller_asset_max_bid = self.group.get_asset_max_bid(self.id_in_group)
			seller_asset_true_value = self.group.get_asset_true_value(self.id_in_group)

			self.round_earning = seller_asset_max_bid - seller_asset_true_value

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
