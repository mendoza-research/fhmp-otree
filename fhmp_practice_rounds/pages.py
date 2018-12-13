from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class SellerChoice(Page):
	form_model = 'group'

	form_fields = ['asset1_disclose_interval']

	def is_displayed(self):
		return self.player.role() == 'seller'

	def before_next_page(self):
		pass


class ResultsWaitPage(WaitPage):
	def after_all_players_arrive(self):
		pass


class BuyerChoice(Page):
	form_model = 'player'
	form_fields = ['bid_asset1', 'bid_asset2']

	def is_displayed(self):
		return self.player.role() == 'buyer'

	def vars_for_template(self):
		return {
			'asset1_disclose_interval': self.group.asset1_disclose_interval,
			'asset2_disclose_interval': self.group.asset2_disclose_interval,
		}


class Results(Page):
	pass


page_sequence = [
	SellerChoice,
	ResultsWaitPage,
	BuyerChoice,
	ResultsWaitPage,
	Results
]
