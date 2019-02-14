from ._builtin import Page, WaitPage

# This is a transition page that is not shown to the end-user
#
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

	# Input text fields to be shown to buyers
	form_fields = ['bid_asset1', 'bid_asset2', 'bid_asset3']

	# is_displayed() is used to show this page only to the buyers
	def is_displayed(self):
		return self.player.role() == 'buyer'

	def vars_for_template(self):
		return {

		}


# This is a transition page that is not shown to the end-user
# Bid winners and payoffs for all players are determined here
class ResultsWaitPage(WaitPage):
	def after_all_players_arrive(self):
		self.group.determine_bid_winners()
		self.group.set_payoffs()


class Results(Page):
	def vars_for_template(self):
		return {
			# This array of objects is used in the Results page to display range of high asset probabilities, true asset value, other players' bids, and winners
			'assets': [
				{
					'asset_id': 1,
					'disclose_interval': self.group.asset1_disclose_interval,
					'asset_value': self.group.asset1_true_value,
					'bid_winner': 1
				},
				{
					'asset_id': 2,
					'disclose_interval': self.group.asset1_disclose_interval,
					'asset_value': self.group.asset1_true_value,
					'bid_winner': 1
				},
				{
					'asset_id': 3,
					'disclose_interval': self.group.asset1_disclose_interval,
					'asset_value': self.group.asset1_true_value,
					'bid_winner': 1
				},
			],
			'payoff': self.player.payoff
		}


page_sequence = [
	BeginWaitPage,
	SellerChoice,
	AllPlayersArrivalWaitPage,
	BuyerChoice,
	ResultsWaitPage,
	Results
]
