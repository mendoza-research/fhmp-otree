from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

author = 'Kimberly Mendoza'

doc = """
Setup rounds
"""


class Constants(BaseConstants):
    name_in_url = 'fhmp_tutorial'
    players_per_group = None
    num_rounds = 1

    # Set the number of sellers
    # Any participants after the number of sellers will be assigned as buyers
    num_sellers = 3

    cc_tf_choices = [
        [True, 'True'],
        [False, 'False'],
    ]

    cc_questions_answers = {
        'Introduction': [
            {
                'label': 'Each round, buyers can bid on up to 3 assets because there are 3 sellers.',
                'choices': cc_tf_choices,
                'correct_answer': True,
                'answer_label': 'True! Each round, buyers can bid on up to 3 assets because there are 3 sellers.'
            },
            {
                'label': 'Buyers will earn more points by winning assets at lower prices.',
                'choices': cc_tf_choices,
                'correct_answer': True,
                'answer_label': 'True! Buyers will earn more points by winning assets at lower prices.'
            },
            {
                'label': 'Sellers will earn more points by selling assets at higher prices.',
                'choices': cc_tf_choices,
                'correct_answer': True,
                'answer_label': 'True! Sellers will earn more points by selling assets at higher prices.'
            },
            {
                'label': 'The more points you earn, the more money you will be paid.',
                'choices': cc_tf_choices,
                'correct_answer': True,
                'answer_label': 'True! The more points you earn, the more money you will be paid.'
            }
        ],
        'AssetDistribution': [
            {
                'label': 'If the seller receives the Private Range 11-13, what is the likelihood 18 will be the true value of the asset?',
                'choices': [
                    ["43%", "43%"],
                    ["20%", "20%"],
                    ["5%", "5%"],
                    ["1%", "1%"]
                ],
                'correct_answer': "1%",
                'answer_label': '1%! There is about a 1% chance the asset\'s true value will be any other number than 11, 12, or 13.'
            },
            {
                'label': 'If the seller receives the Private Range 11-13, what is the likelihood 11 will be the true value of the asset?',
                'choices': [
                    ["43%", "43%"],
                    ["20%", "20%"],
                    ["5%", "5%"],
                    ["1%", "1%"]
                ],
                'correct_answer': '20%',
                'answer_label': '20%! There is a 20% chance the asset\'s true value will be the lowest number in the Private Range.'
            },
            {
                'label': 'If a seller receives the Private Range 13-15, then 14 is the most likely value to be drawn for the asset.',
                'choices': cc_tf_choices,
                'correct_answer': True,
                'answer_label': 'True! The midpoint of the Private Range the seller receives has the highest chance (43%) of being the value drawn for the asset.'
            }
        ],
        'SellerReporting': [
            {
                'label': 'Only the seller knows the Private Range they are given.',
                'choices': cc_tf_choices,
                'correct_answer': True,
                'answer_label': 'True! Only the seller knows the Private Range; no other person in the study knows the Private Range the seller was given.'
            },
            {
                'label': 'Sellers can choose any range they want, as long as it is either 3 or 5 numbers wide, and sellers\' Reported Range does not have to contain any number from the Private Range they were given.',
                'choices': cc_tf_choices,
                'correct_answer': True,
                'answer_label': 'True! The seller can report either a range that is 3 or 5 numbers wide. The seller can also report any range. That is, the seller\'s Reported Range does not have to contain any number from the Private Range they were given.',
                'treatment': 'choice'
            },
            {
                'label': 'Sellers can choose any range they want, as long as it is 3 numbers wide, and sellers\' Reported Range does not have to contain any number from the Private Range they were given.',
                'choices': cc_tf_choices,
                'correct_answer': True,
                'answer_label': 'True! The seller reports a range that is 3 numbers wide. The seller can also report any range. That is, the seller\'s Reported Range does not have to contain any number from the Private Range they were given.',
                'treatment': 'no_choice'
            },
            {
                'label': 'To report a more precise range, sellers must pay 2 points.',
                'choices': cc_tf_choices,
                'correct_answer': True,
                'answer_label': 'True! The seller must pay 2 points if they choose to report the more precise (3-number) range.',
                'treatment': 'choice'
            },
            {
                'label': 'Sellers report ',
                'choices': [
                    [
                        'a single number to the buyers',
                        'a single number to the buyers'],
                    [
                        'a range of 3 numbers(if they pay 2 points)',
                        'a range of 3 numbers(if they pay 2 points)'
                    ],
                    [
                        'a range of 5 numbers',
                        'a range of 5 numbers'
                    ],
                    [
                        'the true value',
                        'the true value'
                    ],
                    [
                        'B or C',
                        'B or C'
                    ]
                ],
                'correct_answer': 'B or C',
                'answer_label': 'B or C! The seller can report either 3 or 5 numbers range. To report a 3 number range, the seller must pay 2 points.',
                'treatment': 'choice'
            }
        ],
        'FactChecker': [
            {
                'label': 'The fact checker is automated.',
                'choices': cc_tf_choices,
                'correct_answer': True,
                'answer_label': 'True! The fact checker is automated.'
            },
            {
                'label': 'The fact checker\'s grade (A, B, C, or F) designating how close the seller\'s Reported Range is to the midpoint of the Fact Checker Range always perfectly corresponds to the true value of the asset.',
                'choices': cc_tf_choices,
                'correct_answer': False,
                'answer_label': 'False. The Fact Checker\'s 5 number range is drawn from a distribution of ranges surrounding the midpoint of the seller\'s Private Range, and it does not perfectly correspond to the true value of the asset.',
                'treatment': 'grade'
            },
            {
                'label': 'The fact checker\'s grade (Pass or Fail) designating how close the seller\'s Reported Range is to the midpoint of the Fact Checker Range always perfectly corresponds to the true value of the asset.',
                'choices': cc_tf_choices,
                'correct_answer': False,
                'answer_label': 'False. The Fact Checker\'s 5 number range is drawn from a distribution of ranges surrounding the midpoint of the seller\'s Private Range, and it does not perfectly correspond to the true value of the asset.',
                'treatment': 'pass_fail'
            },
            {
                'label': 'The fact checker knows',
                'choices': [
                    [
                        'the Private Range the seller receives',
                        'the Private Range the seller receives'
                    ],
                    [
                        'The Fact Checker Range that contains the midpoint of the seller\'s Private Range',
                        'The Fact Checker Range that contains the midpoint of the seller\'s Private Range'
                    ],
                    [
                        'The true value of the asset',
                        'The true value of the asset'
                    ]
                ],
                'correct_answer': 'The Fact Checker Range that contains the midpoint of the seller\'s Private Range',
                'answer_label': 'The Fact Checker knows a 5-number range containing the midpoint of the seller\'s Private Range. It does not know the Private Range the seller receives nor the true value of the asset.'
            }
        ],
        'BuyerBid': [
            {
                'label': 'Buyers can bid on assets.',
                'choices': cc_tf_choices,
                'correct_answer': True,
                'answer_label': 'True! The buyer can bid on as many assets as they want.'
            },
            {
                'label': 'The buyer who bids the most for an asset wins that asset.',
                'choices': cc_tf_choices,
                'correct_answer': True,
                'answer_label': 'True! Highest bidder for each asset will win that asset.'
            },
            {
                'label': 'Sellers earn the winning bid for their asset.',
                'choices': cc_tf_choices,
                'correct_answer': True,
                'answer_label': 'True! Sellers earn whatever the highest bid was for their asset.'
            },
            {
                'label': 'If a buyer has the second highest bid on one asset, the third highest bid on one asset and the highest bid on two assets, the buyer pays for how many assets and receives how many assets?',
                'choices': [
                    ['1 and 1', '1 and 1'],
                    ['2 and 2', '2 and 2'],
                    ['3 and 3', '3 and 3'],
                    ['4 and 4', '4 and 4'],
                    ['5 and 5', '5 and 5']
                ],
                'correct_answer': "2 and 2",
                'answer_label': 'For each asset, the buyer that bids the highest amount of points wins the asset. Since the buyer had the highest bids on 2 assets, he pays for and receives 2 assets.'
            }
        ],
        'EarnPoints': [
            {
                'label': 'Buyers earn 0 points if they are not the highest bid, but if a buyer has the winning bid the buyer earns the true value of the asset less the amount paid for the asset.',
                'choices': cc_tf_choices,
                'correct_answer': True,
                'answer_label': 'True! Losing buyers and buyers that did not bid earn 0 points. Winning buyer earns the true value of the asset less the bid amount.'
            },
            {
                'label': 'Sellers earn the top bid for their asset.',
                'choices': cc_tf_choices,
                'correct_answer': True,
                'answer_label': 'True! Sellers earn whatever the highest bid was for their asset.'
            }
        ],
        'Else': [
            {
                'label': '',
                'choices': None,
                'correct_answer': None,
                'answer_label': ''
            },

        ]
    }


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


# A utility method to create a boolean field for Comprehension Check question answers
def create_cc_boolean_field(question_info):
    return models.BooleanField(
        label=question_info['label'],
        choices=question_info['choices'],
        widget=widgets.RadioSelect
    )


def create_cc_string_field(question_info):
    return models.StringField(
        label=question_info['label'],
        choices=question_info['choices'],
        widget=widgets.RadioSelect
    )

# Assign seller and buyer here for practice and main rounds
# Save the role into participant vars dictionary to use the same
# role for future rounds


t = Constants.cc_questions_answers


class Player(BasePlayer):
    Sona_ID = models.StringField(
        label='Please enter your Sona ID'
    )

    cc_intro_0 = create_cc_boolean_field(t['Introduction'][0])
    cc_intro_1 = create_cc_boolean_field(t['Introduction'][1])
    cc_intro_2 = create_cc_boolean_field(t['Introduction'][2])
    cc_intro_3 = create_cc_boolean_field(t['Introduction'][3])

    cc_asset_0 = create_cc_string_field(t['AssetDistribution'][0])
    cc_asset_1 = create_cc_string_field(t['AssetDistribution'][1])
    cc_asset_2 = create_cc_boolean_field(t['AssetDistribution'][2])

    cc_seller_0 = create_cc_boolean_field(t['SellerReporting'][0])
    cc_seller_1_choice = create_cc_boolean_field(t['SellerReporting'][1])
    cc_seller_2_no_choice = create_cc_boolean_field(t['SellerReporting'][2])
    cc_seller_3_choice = create_cc_boolean_field(t['SellerReporting'][3])
    cc_seller_4_choice = create_cc_string_field(t['SellerReporting'][4])

    cc_fact_checker_0 = create_cc_boolean_field(t['FactChecker'][0])
    cc_fact_checker_1_grade = create_cc_boolean_field(t['FactChecker'][1])
    cc_fact_checker_2_pass_fail = create_cc_boolean_field(t['FactChecker'][2])
    cc_fact_checker_3 = create_cc_string_field(t['FactChecker'][3])

    cc_buyer_bid_0 = create_cc_boolean_field(t['BuyerBid'][0])
    cc_buyer_bid_1 = create_cc_boolean_field(t['BuyerBid'][1])
    cc_buyer_bid_2 = create_cc_boolean_field(t['BuyerBid'][2])
    cc_buyer_bid_3 = create_cc_string_field(t['BuyerBid'][3])

    cc_earn_points_0 = create_cc_boolean_field(t['EarnPoints'][0])
    cc_earn_points_1 = create_cc_boolean_field(t['EarnPoints'][1])

    def role(self):
        if self.id_in_group <= Constants.num_sellers:
            self.participant.vars['role'] = 'seller'

        else:
            self.participant.vars['role'] = 'buyer'

        return self.participant.vars['role']
