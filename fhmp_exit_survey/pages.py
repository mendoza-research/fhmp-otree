from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class ExitSurvey(Page):
    form_model = 'player'
    form_fields = ['gpa', 'gender', 'is_english_first_language',
                   'major', 'years_in_college', 'age', 'comments']


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        pass


page_sequence = [
    ExitSurvey,
    ResultsWaitPage
]
