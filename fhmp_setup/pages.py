from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


# Instruction: Ground rules
class GroundRules(Page):
	pass


# Instruction: How you will get paid
class HowWillYouGetPaid(Page):
	pass


# Instruction: How to earn points
class HowToEarnPoints(Page):
	def vars_for_template(self):
		return {
			'player': self.player,
			'role': self.player.role,
		}


# Background
class Background(Page):
	pass


# Wait for all players to arrive
class ResultsWaitPage(WaitPage):
	def after_all_players_arrive(self):
		pass


page_sequence = [
	GroundRules,
	# HowWillYouGetPaid,
	HowToEarnPoints,
	# Background,
	ResultsWaitPage
]
