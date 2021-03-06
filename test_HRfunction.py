import pytest
import datetime
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
    p = create_patient("199", "alan.regsiter@duke.edu", 23)
    assert p.user_age == 23
    assert p.attending_email == "alan.regsiter@duke.edu"
    assert p.patient_id == "199"


def test_update_heart_rate():
    update_heart_rate("199", 120)
    hr = get_heart_rate("199")
    assert hr[-1] == 120


def test_cal_average_heart_rate():
    update_heart_rate("199", 122)
    hr = get_heart_rate("199")
    assert cal_average_heart_rate(hr) == 121


def test_get_interval_average_heart_rate():
    heart_rates = [100, 150, 200, 100]
    time = datetime.datetime.now()
    heart_rates_time = [time-datetime.timedelta(minutes=2),
                        time,
                        time+datetime.timedelta(minutes=2),
                        time+datetime.timedelta(seconds=2)
                        ]
    avg_hr = get_interval_average_heart_rate(heart_rates, heart_rates_time, time)
    assert avg_hr == (150+200+100)/3


def test_get_status():
    r = get_status("199")
    assert r["is_tachycardic"] is True
    assert r["timestamp"] <= datetime.datetime.now()


def test_get_heart_rate():
    hr = get_heart_rate("199")
    assert hr[-1] == 122
