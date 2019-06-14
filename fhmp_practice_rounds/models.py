import random

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
	initial_endowment = c(20) * num_rounds
	high_detail_disclosure_cost = c(2)
	asset_high_quality_value = c(20)
	asset_low_quality_value = c(1)

	disclose_intervals = {
		'1-5': {
			'label': 'Low: 1-5',
			'cost': 0
		},
		'2-6': {
			'label': 'Low: 2-6',
			'cost': 0
		},
		'3-7': {
			'label': 'Low: 3-7',
			'cost': 0
		},
		'4-8': {
			'label': 'Low: 4-8',
			'cost': 0
		},
		'5-9': {
			'label': 'Low: 5-9',
			'cost': 0
		},
		'6-10': {
			'label': 'Low: 6-10',
			'cost': 0
		},
		'7-11': {
			'label': 'Low: 7-11',
			'cost': 0
		},
		'8-12': {
			'label': 'Low: 8-12',
			'cost': 0
		},
		'9-13': {
			'label': 'Low: 9-13',
			'cost': 0
		},
		'10-14': {
			'label': 'Low: 10-14',
			'cost': 0
		},
		'11-15': {
			'label': 'Low: 11-15',
			'cost': 0
		},
		'12-16': {
			'label': 'Low: 12-16',
			'cost': 0
		},
		'13-17': {
			'label': 'Low: 13-17',
			'cost': 0
		},
		'14-18': {
			'label': 'Low: 14-18',
			'cost': 0
		},
		'15-19': {
			'label': 'Low: 15-19',
			'cost': 0
		},
		'16-20': {
			'label': 'Low: 16-20',
			'cost': 2
		},
		'1-3': {
			'label': 'High: 1-3',
			'cost': 2
		},
		'2-4': {
			'label': 'High: 2-4',
			'cost': 2
		},
		'3-5': {
			'label': 'High: 3-5',
			'cost': 2
		},
		'4-6': {
			'label': 'High: 4-6',
			'cost': 2
		},
		'5-7': {
			'label': 'High: 5-7',
			'cost': 2
		},
		'6-8': {
			'label': 'High: 6-8',
			'cost': 2
		},
		'7-9': {
			'label': 'High: 7-9',
			'cost': 2
		},
		'8-10': {
			'label': 'High: 8-10',
			'cost': 2
		},
		'9-11': {
			'label': 'High: 9-11',
			'cost': 2
		},
		'10-12': {
			'label': 'High: 10-12',
			'cost': 2
		},
		'11-13': {
			'label': 'High: 11-13',
			'cost': 2
		},
		'12-14': {
			'label': 'High: 12-14',
			'cost': 2
		},
		'13-15': {
			'label': 'High: 13-15',
			'cost': 2
		},
		'14-16': {
			'label': 'High: 14-16',
			'cost': 2
		},
		'15-17': {
			'label': 'High: 15-17',
			'cost': 2
		},
		'16-18': {
			'label': 'High: 16-18',
			'cost': 2
		},
		'17-19': {
			'label': 'High: 17-19',
			'cost': 2
		},
		'18-20': {
			'label': 'High: 18-20',
			'cost': 2
		}
	}

	# Create a list of strings to be displayed in form fields
	# shown to users
	disclose_interval_choices = list(map(lambda x: [x[0], x[1]['label']], disclose_intervals.items()))

	# Choices for disclosure levels
	asset_disclose_choices = [
		[False, 'Low (No cost)'],
		[True, 'High (2 points)'],
	]


class Subsession(BaseSubsession):
	def creating_session(self):
		print('creating_session')

		pass

class Group(BaseGroup):
	print('running Group init')

	# Since there is a fixed number of assets, each asset's probability and disclose_interval should be listed here
	asset1_est_value = models.FloatField(min=1.0, max=20.0)
	asset2_est_value = models.FloatField(min=1.0, max=20.0)
	asset3_est_value = models.FloatField(min=1.0, max=20.0)

	# These boolean fields indicate whether the user has selected high (2 points) level
	# of disclosure
	asset1_disclose_high = models.BooleanField(
		choices=Constants.asset_disclose_choices,
		widget=widgets.RadioSelect
	)

	asset2_disclose_high = models.BooleanField(
		choices=Constants.asset_disclose_choices,
		widget=widgets.RadioSelect
	)

	asset3_disclose_high = models.BooleanField(
		choices=Constants.asset_disclose_choices,
		widget=widgets.RadioSelect
	)

	# Disclosure intervals
	asset1_disclose_interval = models.StringField(
		choices=Constants.disclose_interval_choices,
		widget=widgets.RadioSelect,
		blank=False
	)

	asset2_disclose_interval = models.StringField(
		choices=Constants.disclose_interval_choices,
		widget=widgets.RadioSelect,
		# TODO: Remove initial value, for testing only
		initial=Constants.disclose_interval_choices[5][0],
		blank=False
	)

	asset3_disclose_interval = models.StringField(
		choices=Constants.disclose_interval_choices,
		widget=widgets.RadioSelect,
		# TODO: Remove initial value, for testing only
		initial=Constants.disclose_interval_choices[1][0],
		blank=False
	)

	# Assets' true values based on each probability
	asset1_true_value = models.CurrencyField()
	asset2_true_value = models.CurrencyField()
	asset3_true_value = models.CurrencyField()

	asset1_max_bid = models.CurrencyField()
	asset2_max_bid = models.CurrencyField()
	asset3_max_bid = models.CurrencyField()

	# Generate probabilities for each asset and true values
	# Probabilities are in decimal format (examples: 0.173, 0.552, 0.993)
	def init_assets(self):
		# High asset probabilities
		self.asset1_est_value = round(random.uniform(1, 20), 0)
		self.asset2_est_value = round(random.uniform(1, 20), 0)
		self.asset3_est_value = round(random.uniform(1, 20), 0)

		# Asset true values (either low quality or high quality)
		self.asset1_true_value = Constants.asset_high_quality_value if random.random() < self.asset1_est_value else Constants.asset_low_quality_value
		self.asset2_true_value = Constants.asset_high_quality_value if random.random() < self.asset2_est_value else Constants.asset_low_quality_value
		self.asset3_true_value = Constants.asset_high_quality_value if random.random() < self.asset3_est_value else Constants.asset_low_quality_value

	# Set players' budgets for current round
	# budget for current round = budget for prev round - [sum of all winning bids from prev round)
	def set_players_budgets(self):
		for p in self.get_players():
			if p.role() == 'seller':
				p.budget = 5
			else:
				if self.round_number == 1:
					p.budget = Constants.initial_endowment
				else:
					# Get leftover budget from previous round
					p_in_prev_round = p.in_round(self.round_number - 1)
					p.budget = p_in_prev_round.budget

					# If the buyer has purchased an asset through auction in the previous round, deduct the spent amount from budget
					if p_in_prev_round.did_win_asset1:
						p.budget -= p_in_prev_round.bid_asset1

					if p_in_prev_round.did_win_asset2:
						p.budget -= p_in_prev_round.bid_asset2

					if p_in_prev_round.did_win_asset3:
						p.budget -= p_in_prev_round.bid_asset3

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
		return list(map(lambda b: b.id_in_group, self.get_buyers))

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
			# Add bids on each asset to corresponding array
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

	# Set payoffs for all players
	def set_payoffs(self):
		for p in self.get_players():
			p.set_payoff()

	# Get max bids for an asset by asset's seller id
	def get_asset_max_bid(self, seller_id):
		assets = {
			1: self.asset1_max_bid,
			2: self.asset2_max_bid,
			3: self.asset3_max_bid
		}

		return assets[seller_id]


	def get_seller_disclosure_cost(self, seller_id):
		seller_disclose_intervals = {
			1: self.asset1_disclose_interval,
			2: self.asset2_disclose_interval,
			3: self.asset3_disclose_interval
		}

		return Constants.disclose_intervals[seller_disclose_intervals[seller_id]]['cost']


class Player(BasePlayer):
	# Buyer budget for all rounds
	# For practice rounds, buyer budget is 600 (2 rounds * initial endowment)
	# For main rounds, buyer budget is 6000 (20 rounds * initial endowment)
	budget = models.CurrencyField(min=0, blank=False)

	# For buyers
	# Bids on assets
	bid_asset1 = models.CurrencyField(min=0, max=20.0, blank=False)
	bid_asset2 = models.CurrencyField(min=0, max=20.0, blank=False)
	bid_asset3 = models.CurrencyField(min=0, max=20.0, blank=False)

	# For buyers
	# Bids results
	did_win_asset1 = models.BooleanField(initial=False)
	did_win_asset2 = models.BooleanField(initial=False)
	did_win_asset3 = models.BooleanField(initial=False)

	round_earning = models.CurrencyField(min=0, initial=0)

	# Returns 'seller' or 'buyer'
	def role(self):
		return self.participant.vars['role']

	# Calculate earning and add to payoffs
	# This method is run at the end of each round
	def set_payoff(self):
		# Seller earning from round
		if self.role() == 'seller':
			seller_disclosure_cost = self.group.get_seller_disclosure_cost(self.id_in_group)
			seller_asset_max_bid = self.group.get_asset_max_bid(self.id_in_group)

			self.round_earning = seller_asset_max_bid - seller_disclosure_cost

		# Buyer payoffs
		elif self.role() == 'buyer':
			if self.did_win_asset1:
				self.round_earning += self.group.asset1_true_value - self.bid_asset1

			if self.did_win_asset2:
				self.round_earning += self.group.asset2_true_value - self.bid_asset2

			if self.did_win_asset3:
				self.round_earning += self.group.asset3_true_value - self.bid_asset3

		#
		self.payoff += self.round_earning
