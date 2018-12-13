from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
	name_in_url = 'fhmp_tutorial'
	players_per_group = None
	num_rounds = 1

	# Set the number of sellers
	# Any participants after the number of sellers will be assigned as buyers
	num_sellers = 1


class Subsession(BaseSubsession):
	pass


class Group(BaseGroup):
	pass


# Assign seller and buyer here for practice and main rounds
# Save the role into participant vars dictionary to use the same
# role for future rounds
class Player(BasePlayer):
	def role(self):
		if self.id_in_group <= Constants.num_sellers:
			self.participant.vars['role'] = 'seller'

		else:
			self.participant.vars['role'] = 'buyer'

		print('player.id_in_group==', self.id_in_group, ', role=' + self.participant.vars['role'])
		return self.participant.vars['role']
