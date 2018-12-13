from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'my_trust'
    players_per_group = 2
    num_rounds = 1

    endowment = c(10)
    multiplication_factor = 3


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    sent_amount = models.CurrencyField(
        choices=currency_range(0, Constants.endowment, c(1)),
    )
    sent_back_amount = models.CurrencyField()

    pass


class Player(BasePlayer):
    pass
