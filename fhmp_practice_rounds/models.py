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
	initial_endowment = c(300) * num_rounds
	high_detail_disclosure_cost = c(30)
	asset_high_quality_value = c(300)
	asset_low_quality_value = c(100)

	disclose_intervals = {
		'0%-49%': {
			'label': 'Low: 0-49% (No cost)',
			'cost': 0
		},
		'50%-100%': {
			'label': 'Low: 50-100% (No cost)',
			'cost': 0
		},
		'0%-24%': {
			'label': 'High: 0-24% (Costs 30 points)',
			'cost': 30
		},
		'25%-49%': {
			'label': 'High: 25-49% (Costs 30 points)',
			'cost': 30
		},
		'50%-74%': {
			'label': 'High: 50-74% (Costs 30 points)',
			'cost': 30
		},
		'75%-100%': {
			'label': 'High: 75-100% (Costs 30 points)',
			'cost': 30
		}
	}

	disclose_interval_choices = list(map(lambda x: [x[0], x[1]['label']], disclose_intervals.items()))


class Subsession(BaseSubsession):
	def creating_session(self):
		print('creating_session')

		pass

class Group(BaseGroup):
	print('running Group init')

	# Since there is a fixed number of assets, each asset's probability and disclose_interval should be listed here
	asset1_probability = models.FloatField(min=0.0, max=1.0)
	asset2_probability = models.FloatField(min=0.0, max=1.0)
	asset3_probability = models.FloatField(min=0.0, max=1.0)

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
	def init_assets(self):
		self.asset1_probability = round(random.uniform(0, 1), 3)
		self.asset2_probability = round(random.uniform(0, 1), 3)
		self.asset3_probability = round(random.uniform(0, 1), 3)

		self.asset1_true_value = Constants.asset_high_quality_value if random.random() < self.asset1_probability else Constants.asset_low_quality_value
		self.asset2_true_value = Constants.asset_high_quality_value if random.random() < self.asset2_probability else Constants.asset_low_quality_value
		self.asset3_true_value = Constants.asset_high_quality_value if random.random() < self.asset3_probability else Constants.asset_low_quality_value

	# Set players' budgets for current round
	# budget for current round = budget for prev round - [sum of all winning bids from prev round)
	def set_players_budgets(self):
		for p in self.get_players():
			if p.role() == 'seller':
				p.budget = 0
			else:
				if self.round_number == 1:
					p.budget = Constants.initial_endowment
				else:
					# Get leftover budget from previous round
					p_in_prev_round = p.in_round(self.round_number - 1)
					p.budget = p_in_prev_round.budget

					if p_in_prev_round.did_win_asset1:
						p.budget -= p_in_prev_round.bid_asset1

					if p_in_prev_round.did_win_asset2:
						p.budget -= p_in_prev_round.bid_asset2

					if p_in_prev_round.did_win_asset3:
						p.budget -= p_in_prev_round.bid_asset3

	def determine_bid_winners(self):
		group = self

		# A list to hold IDs of all buyers
		buyer_ids = []

		# Lists of bids for each asset by all buyers
		asset1_bids = []
		asset2_bids = []
		asset3_bids = []

		# Lists of max bids for each asset (in case tie happens)
		asset1_max_bidders = []
		asset2_max_bidders = []
		asset3_max_bidders = []

		# For every player
		for p in group.get_players():
			if p.role() == 'buyer':
				# IDs of all buyers
				buyer_ids.append(p.id_in_group)

				# Bids on each asset
				asset1_bids.append(p.bid_asset1)
				asset2_bids.append(p.bid_asset2)
				asset3_bids.append(p.bid_asset3)

		# Get max bid on each asset
		self.asset1_max_bid = max(asset1_bids)
		self.asset2_max_bid = max(asset2_bids)
		self.asset3_max_bid = max(asset3_bids)

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
	bid_asset1 = models.CurrencyField(min=0, blank=True)
	bid_asset2 = models.CurrencyField(min=0, blank=True)
	bid_asset3 = models.CurrencyField(min=0, blank=True)

	# For buyers
	# Bids results
	did_win_asset1 = models.BooleanField(initial=False)
	did_win_asset2 = models.BooleanField(initial=False)
	did_win_asset3 = models.BooleanField(initial=False)

	round_earning = models.CurrencyField(min=0, initial=0)

	# Returns 'seller' or 'buyer'
	def role(self):
		return self.participant.vars['role']

	# Calculate payoff for each player
	def set_payoff(self):
		if self.role() == 'seller':
			seller_disclosure_cost = self.group.get_seller_disclosure_cost(self.id_in_group)
			seller_asset_max_bid = self.group.get_asset_max_bid(self.id_in_group)

			self.round_earning = seller_asset_max_bid - seller_disclosure_cost

		elif self.role() == 'buyer':
			if self.did_win_asset1:
				self.round_earning += self.group.asset1_true_value - self.bid_asset1

			if self.did_win_asset2:
				self.round_earning += self.group.asset2_true_value - self.bid_asset2

			if self.did_win_asset3:
				self.round_earning += self.group.asset3_true_value - self.bid_asset3

		self.payoff += self.round_earning
