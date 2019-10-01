from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

author = 'Your name here'

doc = """
Setup rounds
"""


class Constants(BaseConstants):
    name_in_url = 'fhmp_tutorial'
    players_per_group = None
    num_rounds = 1

    # Set the number of sellers
    # Any participants after the number of sellers will be assigned as buyers
    num_sellers = 2

    CC_tf_choices = [
        [True, 'True'],
        [False, 'False'],
    ]

    CC_QuestionsAnswers = [
        {
            'label': 'Each round, buyers can bid on up to 3 assets because there are 3 sellers.',
            'choices': CC_tf_choices,
            'correct_answer': True,
            'answer_label': 'True! Each round, buyers can bid on up to 3 assets because there are 3 sellers.'
        },
        {
            'label': 'Buyers will earn more points by winning assets at lower prices.',
            'choices': CC_tf_choices,
            'correct_answer': True,
            'answer_label': 'True! Buyers will earn more points by winning assets at lower prices.'
        },
        {
            'label': 'Sellers will earn more points by selling assets at higher prices.',
            'choices': CC_tf_choices,
            'correct_answer': True,
            'answer_label': 'True! Sellers will earn more points by selling assets at higher prices.'
        },
        {
            'label': 'The more points you earn, the more money you will be paid.',
            'choices': CC_tf_choices,
            'correct_answer': True,
            'answer_label': 'True! The more points you earn, the more money you will be paid.'
        },
        {
            'label': 'If the seller receives the number 12, what is the likelihood 18 will be the true value of the asset?',
            'choices': [
                ["30%", "30%"],
                ["18%", "18%"],
                ["5%", "5%"],
                ["2%", "2%"]
            ],
            'correct_answer': "2%",
            'answer_label': '2%! There is about a 2% chance the asset\'s true value will be any other number than 11, 12, or 13.'
        },
        {
            'label': 'If the seller receives the number 12, what is the likelihood 11 will be the true value of the asset?',
            'choices': [
                ["30%", "30%"],
                ["18%", "18%"],
                ["5%", "5%"],
                ["2%", "2%"]
            ],
            'correct_answer': '18%',
            'answer_label': '18%! There is a 18% chance the asset\'s true value will be one less than #.'
        },
        {
            'label': 'If a seller receives the number 14, then 14 is the most likely value to be drawn for the asset.',
            'choices': CC_tf_choices,
            'correct_answer': True,
            'answer_label': 'True! The number seller receives has the highest chance (30%) of being the value drawn for the asset.'
        },
        {
            'label': 'Only the seller knows the number # they are given.',
            'choices': CC_tf_choices,
            'correct_answer': True,
            'answer_label': 'True! Only the seller knows the number #; no other person in the study knows the number the seller was given.'
        },
        {
            'label': 'Sellers can choose any range they want, as long as it is either 3 or 5 numbers wide, and sellers\' Reported Range does not have to contain the number # they were given.',
            'choices': CC_tf_choices,
            'correct_answer': True,
            'answer_label': 'True! The seller can report either 3 or 5 numbers wide. The seller can also report any range. That is, the seller\'s Reported Range does not have to contain the number # they were given.'
        },
        {
            'label': 'To report a more precise range, sellers must pay 2 points.',
            'choices': CC_tf_choices,
            'correct_answer': None,
            'answer_label': 'True! The seller must pay 2 points if they choose to report the more precise (3-number) range.'
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
            'answer_label': 'B or C! The seller can report either 3 or 5 numbers range. To report 5 numbers range, the seller must pay 2 points'
        },
        {
            'label': '',
            'choices': None,
            'correct_answer': None,
            'answer_label': ''
        },
        {
            'label': '',
            'choices': None,
            'correct_answer': None,
            'answer_label': ''
        },
        {
            'label': '',
            'choices': None,
            'correct_answer': None,
            'answer_label': ''
        },
        {
            'label': '',
            'choices': None,
            'correct_answer': None,
            'answer_label': ''
        },
        {
            'label': '',
            'choices': None,
            'correct_answer': None,
            'answer_label': ''
        }
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


# A utility method to create a boolean field for Comprehension Check question answers
def create_cc_boolean_field(question_index):
    return models.BooleanField(
        label=Constants.CC_QuestionsAnswers[question_index]['label'],
        choices=Constants.CC_QuestionsAnswers[question_index]['choices'],
        widget=widgets.RadioSelect
    )


def create_cc_string_field(question_index):
    return models.StringField(
        label=Constants.CC_QuestionsAnswers[question_index]['label'],
        choices=Constants.CC_QuestionsAnswers[question_index]['choices'],
        widget=widgets.RadioSelect
    )

# Assign seller and buyer here for practice and main rounds
# Save the role into participant vars dictionary to use the same
# role for future rounds


class Player(BasePlayer):
    CC0_ans = create_cc_boolean_field(0)
    CC1_ans = create_cc_boolean_field(1)
    CC2_ans = create_cc_boolean_field(2)
    CC3_ans = create_cc_boolean_field(3)

    CC4_ans = create_cc_string_field(4)
    CC5_ans = create_cc_string_field(5)
    CC6_ans = create_cc_boolean_field(6)

    CC7_ans = create_cc_boolean_field(7)
    CC8_ans = create_cc_boolean_field(8)
    CC9_ans = create_cc_boolean_field(9)
    CC10_ans = create_cc_string_field(10)

    def role(self):
        if self.id_in_group <= Constants.num_sellers:
            self.participant.vars['role'] = 'seller'

        else:
            self.participant.vars['role'] = 'buyer'

        return self.participant.vars['role']
