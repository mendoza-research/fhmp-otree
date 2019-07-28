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


# Introduction pages (Kim Added...not sure if they work)
class IntroductionSeller(Page):
	def is_displayed(self):
		return self.player.role() == 'seller'


class IntroductionBuyer(Page):
	def is_displayed(self):
		return self.player.role() == 'buyer'


# Pages discussing the distributions
class Distributions1(Page):
	pass


class Distributions2(Page):
	pass


class Distributions3(Page):
	pass


# All of the instructions (note no longer need the background page
class Instructions1(Page):
	pass


class Instructions2(Page):
	pass


class Instructions3(Page):
	pass


class Instructions4(Page):
	pass


class Instructions5(Page):
	pass


class ExampleRound(Page):
	pass


class CC1(Page):
	form_model = 'player'

	def get_form_fields(self):
		form_fields = ['CC1_ans']
		return form_fields


class CC1_Answer(Page):
	form_model = 'player'

	def vars_for_template(self):

		cc1_choice = self.player.CC1_ans

		return {
			'cc1_choice': cc1_choice
		}


class CC2(Page):
	form_model = 'player'

	def get_form_fields(self):
		form_fields = ['CC2_ans']
		return form_fields


class CC2_Answer(Page):
	form_model = 'player'

	def vars_for_template(self):

		cc2_choice = self.player.CC2_ans

		return {
			'cc2_choice': cc2_choice
		}


class CC3(Page):
	form_model = 'player'

	def get_form_fields(self):
		form_fields = ['CC3_ans']
		return form_fields


class CC3_Answer(Page):
	form_model = 'player'

	def vars_for_template(self):

		cc3_choice = self.player.CC3_ans

		return {
			'cc3_choice': cc3_choice
		}


class CC4(Page):
	form_model = 'player'

	def get_form_fields(self):
		form_fields = ['CC4_ans']
		return form_fields


class CC4_Answer(Page):
	form_model = 'player'

	def vars_for_template(self):

		cc4_choice = self.player.CC4_ans

		return {
			'cc4_choice': cc4_choice
		}


class CC5(Page):
	form_model = 'player'

	def get_form_fields(self):
		form_fields = ['CC5_ans']
		return form_fields


class CC5_Answer(Page):
	form_model = 'player'

	def vars_for_template(self):

		cc5_choice = self.player.CC5_ans

		return {
			'cc5_choice': cc5_choice
		}


class CC6(Page):
	form_model = 'player'

	def get_form_fields(self):
		form_fields = ['CC6_ans']
		return form_fields


class CC6_Answer(Page):
	form_model = 'player'

	def vars_for_template(self):

		cc6_choice = self.player.CC6_ans

		return {
			'cc6_choice': cc6_choice
		}


class CC7(Page):
	form_model = 'player'

	def get_form_fields(self):
		form_fields = ['CC7_ans']
		return form_fields


class CC7_Answer(Page):
	form_model = 'player'

	def vars_for_template(self):

		cc7_choice = self.player.CC7_ans

		return {
			'cc7_choice': cc7_choice
		}


class CC8(Page):
	form_model = 'player'

	def get_form_fields(self):
		form_fields = ['CC8_ans']
		return form_fields


class CC8_Answer(Page):
	form_model = 'player'

	def vars_for_template(self):

		cc8_choice = self.player.CC8_ans

		return {
			'cc8_choice': cc8_choice
		}


class CC9(Page):
	form_model = 'player'

	def get_form_fields(self):
		form_fields = ['CC9_ans']
		return form_fields


class CC9_Answer(Page):
	form_model = 'player'

	def vars_for_template(self):

		cc9_choice = self.player.CC9_ans

		return {
			'cc9_choice': cc9_choice
		}


class CC10(Page):
	form_model = 'player'

	def get_form_fields(self):
		form_fields = ['CC10_ans']
		return form_fields


class CC10_Answer(Page):
	form_model = 'player'

	def vars_for_template(self):

		cc10_choice = self.player.CC10_ans

		return {
			'cc10_choice': cc10_choice
		}


class CC11(Page):
	form_model = 'player'

	def get_form_fields(self):
		form_fields = ['CC11_ans']
		return form_fields


class CC11_Answer(Page):
	form_model = 'player'

	def vars_for_template(self):

		cc11_choice = self.player.CC11_ans

		return {
			'cc11_choice': cc11_choice
		}


class CC12(Page):
	form_model = 'player'

	def get_form_fields(self):
		form_fields = ['CC12_ans']
		return form_fields


class CC12_Answer(Page):
	form_model = 'player'

	def vars_for_template(self):

		cc12_choice = self.player.CC12_ans

		return {
			'cc12_choice': cc12_choice
		}


class CC13(Page):
	form_model = 'player'

	def get_form_fields(self):
		form_fields = ['CC13_ans']
		return form_fields


class CC13_Answer(Page):
	form_model = 'player'

	def vars_for_template(self):

		cc13_choice = self.player.CC13_ans

		return {
			'cc13_choice': cc13_choice
		}


class CC14(Page):
	form_model = 'player'

	def get_form_fields(self):
		form_fields = ['CC14_ans']
		return form_fields


class CC14_Answer(Page):
	form_model = 'player'

	def vars_for_template(self):

		cc14_choice = self.player.CC14_ans

		return {
			'cc14_choice': cc14_choice
		}


class CC15(Page):
	form_model = 'player'

	def get_form_fields(self):
		form_fields = ['CC15_ans']
		return form_fields


class CC15_Answer(Page):
	form_model = 'player'

	def vars_for_template(self):

		cc15_choice = self.player.CC15_ans

		return {
			'cc15_choice': cc15_choice
		}


class CC16(Page):
	form_model = 'player'

	def get_form_fields(self):
		form_fields = ['CC16_ans']
		return form_fields


class CC16_Answer(Page):
	form_model = 'player'

	def vars_for_template(self):

		cc16_choice = self.player.CC16_ans

		return {
			'cc16_choice': cc16_choice
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
	IntroductionSeller,
	IntroductionBuyer,
	Distributions1,
	Distributions2,
	Distributions3,
	Instructions1,
	Instructions2,
	Instructions3,
	Instructions4,
	Instructions5,
	HowWillYouGetPaid,
	ExampleRound,
	CC1,
	CC1_Answer,
	CC2,
	CC2_Answer,
	CC3,
	CC3_Answer,
	CC4,
	CC4_Answer,
	CC5,
	CC5_Answer,
	CC6,
	CC6_Answer,
	CC7,
	CC7_Answer,
	CC8,
	CC8_Answer,
	CC9,
	CC9_Answer,
	CC10,
	CC10_Answer,
	CC11,
	CC11_Answer,
	CC12,
	CC12_Answer,
	CC13,
	CC13_Answer,
	CC14,
	CC14_Answer,
	CC15,
	CC15_Answer,
	CC16,
	CC16_Answer,
	ResultsWaitPage
]
