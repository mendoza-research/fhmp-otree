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
class CC_Introduction(Page):
    form_model = 'player'

    def get_form_fields(self):
        form_fields = [
            'CC_Intro0',
            'CC_Intro1',
            'CC_Intro2',
            'CC_Intro3'
        ]
        return form_fields


# Comprehension Check 1 - Answer
class CC_Introduction_Answers(Page):
    form_model = 'player'

    def vars_for_template(self):
        player_choices = [
            self.player.CC_Intro0,
            self.player.CC_Intro1,
            self.player.CC_Intro2,
            self.player.CC_Intro3
        ]

        questions_answers = []

        for idx, qa in enumerate(Constants.CC_QuestionsAnswers['Introduction']):
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
class CC_AssetDistribution(Page):
    form_model = 'player'

    def get_form_fields(self):
        form_fields = [
            'CC_Asset0',
            'CC_Asset1',
            'CC_Asset2'
        ]
        return form_fields


# Comprehension Check 2 - Answer
class CC_AssetDistribution_Answers(Page):
    form_model = 'player'

    def vars_for_template(self):
        player_choices = [
            self.player.CC_Asset0,
            self.player.CC_Asset1,
            self.player.CC_Asset2
        ]

        questions_answers = []

        for idx, qa in enumerate(Constants.CC_QuestionsAnswers['AssetDistribution']):
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
class CC_SellerReporting(Page):
    form_model = 'player'

    def get_form_fields(self):
        form_fields = [
            'CC_Seller0',
            'CC_Seller1',
            'CC_Seller2',
            'CC_Seller3'
        ]
        return form_fields


# Comprehension Check 2 - Answer
class CC_SellerReporting_Answers(Page):
    form_model = 'player'

    def vars_for_template(self):
        player_choices = [
            self.player.CC_Seller0,
            self.player.CC_Seller1,
            self.player.CC_Seller2,
            self.player.CC_Seller3
        ]

        questions_answers = []

        for idx, qa in enumerate(Constants.CC_QuestionsAnswers['SellerReporting']):
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


class InstructionsFactCheckerExamples(Page):
    pass


class CC_FactChecker(Page):
    form_model = 'player'

    def get_form_fields(self):
        form_fields = [
            'CC_FactChecker0',
            'CC_FactChecker1',
            'CC_FactChecker2'
        ]
        return form_fields


class CC_FactChecker_Answers(Page):
    form_model = 'player'

    def vars_for_template(self):
        player_choices = [
            self.player.CC_FactChecker0,
            self.player.CC_FactChecker1,
            self.player.CC_FactChecker2
        ]

        questions_answers = []

        for idx, qa in enumerate(Constants.CC_QuestionsAnswers['FactChecker']):
            qa_copy = qa.copy()
            qa_copy['player_choice'] = player_choices[idx]
            qa_copy['is_correct'] = player_choices[idx] == qa['correct_answer']
            qa_copy['choices'] = list(map(lambda x: x[0], qa['choices']))
            questions_answers.append(qa_copy)

        return {
            'questions_answers': questions_answers
        }


class InstructionsBuyersBidOnAssets(Page):
    pass


class CC_BuyerBid(Page):
    form_model = 'player'

    def get_form_fields(self):
        form_fields = [
            'CC_BuyerBid0',
            'CC_BuyerBid1',
            'CC_BuyerBid2',
            'CC_BuyerBid3'
        ]
        return form_fields


class CC_BuyerBid_Answers(Page):
    form_model = 'player'

    def vars_for_template(self):
        player_choices = [
            self.player.CC_BuyerBid0,
            self.player.CC_BuyerBid1,
            self.player.CC_BuyerBid2,
            self.player.CC_BuyerBid3
        ]

        questions_answers = []

        for idx, qa in enumerate(Constants.CC_QuestionsAnswers['BuyerBid']):
            qa_copy = qa.copy()
            qa_copy['player_choice'] = player_choices[idx]
            qa_copy['is_correct'] = player_choices[idx] == qa['correct_answer']
            qa_copy['choices'] = list(map(lambda x: x[0], qa['choices']))
            questions_answers.append(qa_copy)

        return {
            'questions_answers': questions_answers
        }


class InstructionsEndOfTheRound(Page):
    pass


class HowWillIEarnPoints(Page):
    pass


class CC_EarnPoints(Page):
    form_model = 'player'

    def get_form_fields(self):
        form_fields = [
            'CC_EarnPoints0',
            'CC_EarnPoints1',
        ]
        return form_fields


class CC_EarnPoints_Answers(Page):
    form_model = 'player'

    def vars_for_template(self):
        player_choices = [
            self.player.CC_EarnPoints0,
            self.player.CC_EarnPoints1,
        ]

        questions_answers = []

        for idx, qa in enumerate(Constants.CC_QuestionsAnswers['EarnPoints']):
            qa_copy = qa.copy()
            qa_copy['player_choice'] = player_choices[idx]
            qa_copy['is_correct'] = player_choices[idx] == qa['correct_answer']
            qa_copy['choices'] = list(map(lambda x: x[0], qa['choices']))
            questions_answers.append(qa_copy)

        return {
            'questions_answers': questions_answers
        }


class PlayerRole(Page):
    def vars_for_template(self):
        return {
            'role': 'Buyer/Seller'
        }


# Wait for all players to arrive
class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        pass


page_sequence = [
    # GroundRules,
    # HowWillIGetPaid,
    # Introduction,
    # CC_Introduction,
    # CC_Introduction_Answers,
    # HowMuchIsAssetWorth,
    # AssetDistribution,
    # AssetDistributionExample,
    # CC_AssetDistribution,
    # CC_AssetDistribution_Answers,
    # InstructionsSellerReceivesNumber,
    # InstructionsSellerChooseReportedRange,
    # CC_SellerReporting,
    # CC_SellerReporting_Answers,
    # InstructionsFactChecker,
    # InstructionsFactCheckerExamples,
    # CC_FactChecker,
    # CC_FactChecker_Answers,
    # InstructionsBuyersBidOnAssets,
    CC_BuyerBid,
    CC_BuyerBid_Answers,
    InstructionsEndOfTheRound,
    HowWillIEarnPoints,
    CC_EarnPoints,
    CC_EarnPoints_Answers,
    PlayerRole,
    # ExampleRound,
    ResultsWaitPage
]
