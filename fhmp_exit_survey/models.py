from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Kimberly Mendoza'

doc = """
Exit survey
"""


class Constants(BaseConstants):
    name_in_url = 'fhmp_exit_survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    gpa = models.FloatField(label='What is your GPA?')
    gender = models.StringField(label='Gender', choices=['Male', 'Female'])
    is_english_first_language = models.BooleanField(
        label='Is English your first language?')
    major = models.StringField(label='What is your major?')
    years_in_college = models.FloatField(
        label='How many years have you been in college?')
    age = models.IntegerField(label='What is your age?')
    comments = models.StringField(
        label='Do you have any questions or comments about the study? If so, please specify below', blank=True)
