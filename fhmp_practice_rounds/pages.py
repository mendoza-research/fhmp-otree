from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

import random

class BeginWaitPage(WaitPage):
	def after_all_players_arrive(self):
		self.group.init_assets()
		self.group.set_players_budgets()


class SellerChoice(Page):
	form_model = 'group'

	form_fields = ['asset1_disclose_interval']

	def is_displayed(self):
		return self.player.role() == 'seller'

	# Return disclose interval form field based on player id
	def get_form_fields(self):
		form_fields_by_player_id = {
			1: ['asset1_disclose_interval'],
			2: ['asset2_disclose_interval'],
			3: ['asset3_disclose_interval']
		}

		return form_fields_by_player_id[self.player.id_in_group]

	def vars_for_template(self):
		asset_probabilities_by_player_id = {
			1: self.group.asset1_probability,
			2: self.group.asset2_probability,
			3: self.group.asset3_probability
		}

		asset_probability_text = "{0:.0f}%".format(asset_probabilities_by_player_id[self.player.id_in_group] * 100)

		return {
			'asset_probability': asset_probability_text
		}

	def before_next_page(self):
		pass


class AllPlayersArrivalWaitPage(WaitPage):
	def after_all_players_arrive(self):
		pass


class BuyerChoice(Page):
	form_model = 'player'
	form_fields = ['bid_asset1', 'bid_asset2', 'bid_asset3']

	def is_displayed(self):
		return self.player.role() == 'buyer'

	def vars_for_template(self):
		return {
			'asset1_disclose_interval': self.group.asset1_disclose_interval,
			'asset2_disclose_interval': self.group.asset2_disclose_interval,
			'asset3_disclose_interval': self.group.asset3_disclose_interval,
		}


class ResultsWaitPage(WaitPage):
	def after_all_players_arrive(self):
		self.group.determine_bid_winners()
		self.group.set_payoffs()


class Results(Page):
	def vars_for_template(self):
		results = {
			sellers: None,
			buyers: None
		}

		pass


page_sequence = [
	BeginWaitPage,
	SellerChoice,
	AllPlayersArrivalWaitPage,
	BuyerChoice,
	ResultsWaitPage,
	Results
]
