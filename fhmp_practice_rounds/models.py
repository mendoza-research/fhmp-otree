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
	initial_endowment = c(300) * num_rounds
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
	def 
	def creating_session(self):
		pass


class Group(BaseGroup):
	# Since there is a fixed number of assets, each asset's probability and disclose_interval should be listed here
	asset1_probability = models.FloatField(min=0.0, max=1.0, initial=round(random.uniform(0, 1), 3))
	asset2_probability = models.FloatField(min=0.0, max=1.0, initial=round(random.uniform(0, 1), 3))
	asset3_probability = models.FloatField(min=0.0, max=1.0, initial=round(random.uniform(0, 1), 3))

	# Disclosure intervals
	asset1_disclose_interval = models.StringField(
		choices=Constants.disclose_interval_choices,
		widget=widgets.RadioSelect,
		blank=False
	)
	asset2_disclose_interval = models.StringField(
		choices=Constants.disclose_interval_choices,
		widget=widgets.RadioSelect,
		initial=Constants.disclose_interval_choices[5][0],
		blank=False
	)
	asset3_disclose_interval = models.StringField(
		choices=Constants.disclose_interval_choices,
		widget=widgets.RadioSelect,
		initial=Constants.disclose_interval_choices[1][0],
		blank=False
	)

	asset1_true_value = models.CurrencyField(initial=Constants.asset_high_quality_value if random.random() < asset1_probability.default else Constants.asset_low_quality_value)
	asset2_true_value = models.CurrencyField(initial=Constants.asset_high_quality_value if random.random() < asset2_probability.default else Constants.asset_low_quality_value)
	asset3_true_value = models.CurrencyField(initial=Constants.asset_high_quality_value if random.random() < asset3_probability.default else Constants.asset_low_quality_value)

class Player(BasePlayer):
	budget = models.CurrencyField(min=0, blank=False)

	# For buyers
	# Bid on assets
	bid_asset1 = models.CurrencyField(min=0, blank=True)
	bid_asset2 = models.CurrencyField(min=0, blank=True)
	bid_asset3 = models.CurrencyField(min=0, blank=True)

	# For buyers
	# Bid result
	did_win_asset1 = models.BooleanField(initial=False)
	did_win_asset2 = models.BooleanField(initial=False)
	did_win_asset3 = models.BooleanField(initial=False)

	# 	if self.round_number == 1:
	# 		p.budget = Constants.initial_endowment
	# 	else:
	# 		p.budget = p.in_previous_rounds

	# Returns 'seller' or 'buyer'
	def role(self):
		print('get p(', self.id_in_group, ').role=', self.participant.vars['role'])
		return self.participant.vars['role']

	def get_payoff(self):
		print('get_payoff for player ', self.id_in_group, ', role=' + self.role())

		if self.role() == 'seller':
			pass

		elif self.role() == 'buyer':
			pass




