from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


# Instruction: Ground rules
class GroundRules(Page):
    pass


# Instruction: How you will get paid
class HowWillIGetPaid(Page):
    pass


# Introduction
class Introduction(Page):
    pass


# Comprehension Check 1
class CC1(Page):
    form_model = 'player'

    def get_form_fields(self):
        form_fields = [
            'CC0_ans',
            'CC1_ans',
            'CC2_ans',
            'CC3_ans'
        ]
        return form_fields


# Comprehension Check 1 - Answer
class CC1_Answer(Page):
    form_model = 'player'

    def vars_for_template(self):
        player_choices = [
            self.player.CC0_ans,
            self.player.CC1_ans,
            self.player.CC2_ans,
            self.player.CC3_ans
        ]

        questions_answers = []

        for idx, qa in enumerate(Constants.CC_QuestionsAnswers[0:4]):
            qa_copy = qa.copy()
            qa_copy['player_choice'] = player_choices[idx]
            qa_copy['is_correct'] = player_choices[idx] == qa['correct_answer']
            qa_copy['choices'] = list(map(lambda x: x[0], qa['choices']))
            questions_answers.append(qa_copy)

        return {
            'questions_answers': questions_answers
        }


# How much is each asset worth?
class HowMuchIsAssetWorth(Page):
    pass


class AssetDistribution(Page):
    pass


class AssetDistributionExample(Page):
    pass


# Comprehension Check 2
class CC2(Page):
    form_model = 'player'

    def get_form_fields(self):
        form_fields = [
            'CC4_ans',
            'CC5_ans',
            'CC6_ans'
        ]
        return form_fields


# Comprehension Check 2 - Answer
class CC2_Answer(Page):
    form_model = 'player'

    def vars_for_template(self):
        player_choices = [
            self.player.CC4_ans,
            self.player.CC5_ans,
            self.player.CC6_ans
        ]

        questions_answers = []

        for idx, qa in enumerate(Constants.CC_QuestionsAnswers[4:7]):
            qa_copy = qa.copy()
            qa_copy['player_choice'] = player_choices[idx]
            qa_copy['is_correct'] = player_choices[idx] == qa['correct_answer']
            qa_copy['choices'] = list(map(lambda x: x[0], qa['choices']))
            questions_answers.append(qa_copy)

        return {
            'questions_answers': questions_answers
        }


class InstructionsSellerReceivesNumber(Page):
    pass


class InstructionsSellerChooseReportedRange(Page):
    pass


# Comprehension Check 2
class CC3(Page):
    form_model = 'player'

    def get_form_fields(self):
        form_fields = [
            'CC7_ans',
            'CC8_ans',
            'CC9_ans',
            'CC10_ans'
        ]
        return form_fields


# Comprehension Check 2 - Answer
class CC3_Answer(Page):
    form_model = 'player'

    def vars_for_template(self):
        player_choices = [
            self.player.CC7_ans,
            self.player.CC8_ans,
            self.player.CC9_ans,
            self.player.CC10_ans
        ]

        questions_answers = []

        for idx, qa in enumerate(Constants.CC_QuestionsAnswers[7:11]):
            qa_copy = qa.copy()
            qa_copy['player_choice'] = player_choices[idx]
            qa_copy['is_correct'] = player_choices[idx] == qa['correct_answer']
            qa_copy['choices'] = list(map(lambda x: x[0], qa['choices']))
            questions_answers.append(qa_copy)

        return {
            'questions_answers': questions_answers
        }


class InstructionsFactChecker(Page):
    pass


class Instructions4(Page):
    pass


class Instructions5(Page):
    pass


# Wait for all players to arrive
class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        pass


page_sequence = [
    GroundRules,
    HowWillIGetPaid,
    Introduction,
    CC1,
    CC1_Answer,
    HowMuchIsAssetWorth,
    AssetDistribution,
    AssetDistributionExample,
    CC2,
    CC2_Answer,
    InstructionsSellerReceivesNumber,
    InstructionsSellerChooseReportedRange,
    CC3,
    CC3_Answer,
    InstructionsFactChecker,
    Instructions4,
    Instructions5,
    # ExampleRound,
    # CC2,
    # CC2_Answer,
    # CC3,
    # CC3_Answer,
    # CC4,
    # CC4_Answer,
    # CC5,
    # CC5_Answer,
    ResultsWaitPage
]
