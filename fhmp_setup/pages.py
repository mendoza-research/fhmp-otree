from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class SonaID(Page):
    form_model = 'player'
    form_fields = ['Sona_ID']


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
            'cc_intro_0',
            'cc_intro_1',
            'cc_intro_2',
            'cc_intro_3'
        ]
        return form_fields


# Comprehension Check 1 - Answer
class CC_Introduction_Answers(Page):
    form_model = 'player'

    def vars_for_template(self):
        player_choices = [
            self.player.cc_intro_0,
            self.player.cc_intro_1,
            self.player.cc_intro_2,
            self.player.cc_intro_3
        ]

        questions_answers = []

        for idx, qa in enumerate(Constants.cc_questions_answers['Introduction']):
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
            'cc_asset_0',
            'cc_asset_1',
            'cc_asset_2'
        ]
        return form_fields


# Comprehension Check 2 - Answer
class CC_AssetDistribution_Answers(Page):
    form_model = 'player'

    def vars_for_template(self):
        player_choices = [
            self.player.cc_asset_0,
            self.player.cc_asset_1,
            self.player.cc_asset_2
        ]

        questions_answers = []

        for idx, qa in enumerate(Constants.cc_questions_answers['AssetDistribution']):
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
            'cc_seller_0',
            'cc_seller_1',
            'cc_seller_2',
            'cc_seller_3'
        ]
        return form_fields


# Comprehension Check 2 - Answer
class CC_SellerReporting_Answers(Page):
    form_model = 'player'

    def vars_for_template(self):
        player_choices = [
            self.player.cc_seller_0,
            self.player.cc_seller_1,
            self.player.cc_seller_2,
            self.player.cc_seller_3
        ]

        questions_answers = []

        for idx, qa in enumerate(Constants.cc_questions_answers['SellerReporting']):
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
            'cc_fact_checker_0',
            'cc_fact_checker_1',
            'cc_fact_checker_2'
        ]
        return form_fields


class CC_FactChecker_Answers(Page):
    form_model = 'player'

    def vars_for_template(self):
        player_choices = [
            self.player.cc_fact_checker_0,
            self.player.cc_fact_checker_1,
            self.player.cc_fact_checker_2
        ]

        questions_answers = []

        for idx, qa in enumerate(Constants.cc_questions_answers['FactChecker']):
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
            'cc_buyer_bid_0',
            'cc_buyer_bid_1',
            'cc_buyer_bid_2',
            'cc_buyer_bid_3'
        ]
        return form_fields


class CC_BuyerBid_Answers(Page):
    form_model = 'player'

    def vars_for_template(self):
        player_choices = [
            self.player.cc_buyer_bid_0,
            self.player.cc_buyer_bid_1,
            self.player.cc_buyer_bid_2,
            self.player.cc_buyer_bid_3
        ]

        questions_answers = []

        for idx, qa in enumerate(Constants.cc_questions_answers['BuyerBid']):
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
            'cc_earn_points_0',
            'cc_earn_points_1',
        ]
        return form_fields


class CC_EarnPoints_Answers(Page):
    form_model = 'player'

    def vars_for_template(self):
        player_choices = [
            self.player.cc_earn_points_0,
            self.player.cc_earn_points_1,
        ]

        questions_answers = []

        for idx, qa in enumerate(Constants.cc_questions_answers['EarnPoints']):
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
            'role': self.player.role()
        }


# Wait for all players to arrive
class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        pass


page_sequence = [
    SonaID,
    GroundRules,
    HowWillIGetPaid,
    Introduction,
    CC_Introduction,
    CC_Introduction_Answers,
    HowMuchIsAssetWorth,
    AssetDistribution,
    AssetDistributionExample,
    CC_AssetDistribution,
    CC_AssetDistribution_Answers,
    InstructionsSellerReceivesNumber,
    InstructionsSellerChooseReportedRange,
    CC_SellerReporting,
    CC_SellerReporting_Answers,
    InstructionsFactChecker,
    InstructionsFactCheckerExamples,
    CC_FactChecker,
    CC_FactChecker_Answers,
    InstructionsBuyersBidOnAssets,
    CC_BuyerBid,
    CC_BuyerBid_Answers,
    InstructionsEndOfTheRound,
    HowWillIEarnPoints,
    CC_EarnPoints,
    CC_EarnPoints_Answers,
    PlayerRole,
    ResultsWaitPage
]
