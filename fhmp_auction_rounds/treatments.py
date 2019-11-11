import os

# A separate file to set treatments

# For local testing
os.environ['CAN_CHOOSE_PRECISION'] = 'True'
os.environ['IS_GRADE_PASS_FAIL'] = 'True'


class Treatments:
    # is_choice indicates whether sellers can choose reporting range precision (less or more precise)
    # if is_choice is False, all sellers are forced to see the more precise option
    # if is_choice is False, reporting cost will be 0
    can_choose_precision = os.getenv(
        'CAN_CHOOSE_PRECISION') == 'True' if 'CAN_CHOOSE_PRECISION' in os.environ else True

    # is_pass_fail indicates whether the fact checker grade should be Pass/Fail or A/B/C/F
    # A,B,C => Pass, D => Fail
    is_grade_pass_fail = os.getenv(
        'IS_GRADE_PASS_FAIL') == 'True' if 'IS_GRADE_PASS_FAIL' in os.environ else True
