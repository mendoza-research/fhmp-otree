from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


# Instruction: Ground rules
class GroundRules(Page):
	pass


# Instruction: How you will get paid
class HowWillYouGetPaid(Page):
	pass


# Background
class Background(Page):
	pass


class MyPage(Page):
	pass


# Wait for all players to arrive
class ResultsWaitPage(WaitPage):
	def after_all_players_arrive(self):
		pass


class Results(Page):
	pass


page_sequence = [
	# GroundRules,
	# HowWillYouGetPaid,
	Background,

	ResultsWaitPage,
	Results
]
