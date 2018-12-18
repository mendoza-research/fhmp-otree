from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

import random


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

		}

		pass

	def before_next_page(self):
		pass


class AllPlayersWaitPage(WaitPage):
	def after_all_players_arrive(self):
		pass


class ResultsWaitPage(WaitPage):
	def after_all_players_arrive(self):
		group = self.group

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

		for p in group.get_players():
			if p.role() == 'buyer':
				# IDs of all buyers
				buyer_ids.append(p.id_in_group)

				# Bids on each asset
				asset1_bids.append(p.bid_asset1)
				asset2_bids.append(p.bid_asset2)
				asset3_bids.append(p.bid_asset3)

		print('buyers in ResultsWaitPage')
		print(buyer_ids)

		print('bids on asset1=', asset1_bids)
		print('bids on asset2=', asset2_bids)
		print('bids on asset3=', asset3_bids)

		# Get max bid on each asset
		asset1_max_bid = max(asset1_bids)
		asset2_max_bid = max(asset2_bids)
		asset3_max_bid = max(asset3_bids)

		print('asset1_max_bid=', asset1_max_bid)
		print('asset2_max_bid=', asset2_max_bid)
		print('asset3_max_bid=', asset3_max_bid)

		for buyer_id in buyer_ids:
			p = group.get_player_by_id(buyer_id)

			if p.bid_asset1 >= asset1_max_bid:
				asset1_max_bidders.append(buyer_id)

			if p.bid_asset2 >= asset2_max_bid:
				asset2_max_bidders.append(buyer_id)

			if p.bid_asset3 >= asset3_max_bid:
				asset3_max_bidders.append(buyer_id)

		print('asset1_max_bidders=', asset1_max_bidders)
		print('asset2_max_bidders=', asset2_max_bidders)
		print('asset3_max_bidders=', asset3_max_bidders)

		# Randomly select a winner amongst highest bidders for each asset
		group.get_player_by_id(random.choice(asset1_max_bidders)).did_win_asset1 = True
		group.get_player_by_id(random.choice(asset2_max_bidders)).did_win_asset2 = True
		group.get_player_by_id(random.choice(asset3_max_bidders)).did_win_asset3 = True



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


class Results(Page):
	pass


page_sequence = [
	SellerChoice,
	AllPlayersWaitPage,
	BuyerChoice,
	ResultsWaitPage,
	Results
]
