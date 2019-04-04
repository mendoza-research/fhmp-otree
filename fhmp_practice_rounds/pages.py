from ._builtin import Page, WaitPage

# Each page that a player sees is defined in this file
# Each class in this file represents a page

# Each page can inherit either a "Page" class or a "WaitPage" class
# If a page inherits a "WaitPage" class, the page is simply a page to wait until
# all players arrive
# Example 1: class BeginWaitPage(Waitpage) is a page class that inherits "WaitPage" class
# This page is not shown to players and is used to wait until all players are on the same page (no pun intended!)

# Example 2: class SellerChoice(Page) is a page that inherits "Page" class
# This page is shown to players

# For detailed documentation regarding pages, please refer to oTree's documentation page below
# https://otree.readthedocs.io/en/latest/pages.html

# This is a transition page that is not shown to the end-user
class BeginWaitPage(WaitPage):
	# This method is called once all players arrive at this page.
	def after_all_players_arrive(self):
		# init_assets() is a method defined in models.py
		# The init_assets() method does two things as described below
		# 1. It generates a random probability for each asset being a "high quality" asset
		# 2. It determines the true asset value based on the probablity generated from Step 1
		self.group.init_assets()
		
		# set_players_budgets() is a method defined in models.py
		# It sets the remaining budget for each player
		
		# For a seller, the budget will always be 0
		
		# For a buyer, two cases exist. 
		# If first round, the budget will be set to initial endowment amount (300 multipled by number of rounds)
		# As an example, if a player has 20 rounds, the initial endowment will be set to 6,000 for the first round
		# If later than first round, budget will be decreased by the amount used in purchasing an asset (with winning bid)
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
			'asset1_disclose_interval': self.group.asset1_disclose_interval,
			'asset2_disclose_interval': self.group.asset2_disclose_interval,
			'asset3_disclose_interval': self.group.asset3_disclose_interval,
		}


# This is a transition page that is not shown to the end-user
# Bid winners and payoffs for all players are determined here
class ResultsWaitPage(WaitPage):
	def after_all_players_arrive(self):
		self.group.determine_bid_winners()
		self.group.set_payoffs()


class Results(Page): 
	def vars_for_template(self):
		buyers = self.group.get_buyers()

		return {
			# This array of objects is used in the Results page
			# to display range of high asset probabilities, true asset value,
			# other buyers' bids, and winners

			'assets': [
				{
					'id': 1,
					'disclose_interval': self.group.asset1_disclose_interval,
					'true_value': self.group.asset1_true_value,
					'bids': list(map(lambda b: {
						'player_id': b.id_in_group,
						'amount': b.bid_asset1,
						'did_win': b.did_win_asset1,
						'is_self': b.id_in_group == self.player.id_in_group
					}, buyers))
				},
				{
					'id': 2,
					'disclose_interval': self.group.asset2_disclose_interval,
					'true_value': self.group.asset2_true_value,
					'bids': list(map(lambda b: {
						'player_id': b.id_in_group,
						'amount': b.bid_asset2,
						'did_win': b.did_win_asset2,
						'is_self': b.id_in_group == self.player.id_in_group
					}, buyers))
				},
				{
					'id': 3,
					'disclose_interval': self.group.asset2_disclose_interval,
					'true_value': self.group.asset3_true_value,
					'bids': list(map(lambda b: {
						'player_id': b.id_in_group,
						'amount': b.bid_asset3,
						'did_win': b.did_win_asset3,
						'is_self': b.id_in_group == self.player.id_in_group
					}, buyers))
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
