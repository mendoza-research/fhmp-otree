import random

from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
	name_in_url = 'fhmp_practice_rounds'
	players_per_group = None

	# Practice = 2 rounds
	# Main = 20 rounds
	num_rounds = 1

	# Currency definitions
	initial_endowment = c(100)
	high_detail_disclosure_cost = c(30)
	asset_high_quality_value = c(300)
	asset_low_quality_value = c(100)

	disclose_interval_choices = [
		['0%-49%', 'Low: 0-49% (No cost)'],
		['50%-100%', 'Low: 50-100% (No cost)'],
		['0%-24%', 'High: 0-24% (Costs 30 points)'],
		['25%-49%', 'High: 25-49% (Costs 30 points)'],
		['50%-74%', 'High: 50-74% (Costs 30 points)'],
		['75%-100%', 'High: 75-100% (Costs 30 points)'],
	]


class Subsession(BaseSubsession):
	pass


class Group(BaseGroup):
	# Since there is a fixed number of assets, each asset's probability and disclose_interval should be listed here
	asset1_probability = models.FloatField(min=0.0, max=1.0, initial=random.uniform(0, 1))
	asset2_probability = models.FloatField(min=0.0, max=1.0, initial=random.uniform(0, 1))

	# Disclosure intervals
	asset1_disclose_interval = models.StringField(
		choices=Constants.disclose_interval_choices,
		widget=widgets.RadioSelect
	)
	asset2_disclose_interval = models.StringField(
		choices=Constants.disclose_interval_choices,
		widget=widgets.RadioSelect,
		initial=Constants.disclose_interval_choices[5][0]
	)

	def set_payoffs(self):
		asset_bids = []

		for player in self.get_players():
			if player.role() == 'buyer':
				asset_bids.append(player.bid_asset1)

		for player in self.get_players():
			if player.role() == 'seller':
				pass


class Player(BasePlayer):
	# For buyers
	# Bid on assets
	bid_asset1 = models.CurrencyField(min=0, blank=False)
	bid_asset2 = models.CurrencyField(min=0, blank=False)

	# Returns 'seller' or 'buyer'
	def role(self):
		return self.participant.vars['role']
