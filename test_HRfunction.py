import pytest
from HRfunction import *


@pytest.mark.parametrize("age, heart_rate, expected", [
    (1, 200, True),
    (2, 150, False),
    (2, 160, True),
    (3, 130, False),
    (3, 160, True),
    (6, 120, False),
    (6, 160, True),
    (10, 70, False),
    (10, 180, True),
    (50, 90, False),
    (50, 120, True),
])
def test_is_tachycardic(age, heart_rate, expected):
    """
    Test is tachycardic based on a set of valuese
    :param age: num
    :param heart_rate: num
    :param expected: True or False
    :return: pass or fail
    """
    assert is_tachycardic(age, heart_rate) == expected

def test_create_patient():
    P = create_patient("199", "alan.regsiter@duke.edu", 15)
    assert P.user_age == 10
    assert P.attending_email == "alan.register@duke.edu"
    assert P.patient_id == "199"

