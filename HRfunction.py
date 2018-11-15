


def is_tachycardic(age, heart_rate):
    """
    Determine if heart_rate is tachycardia based on the person's age
    used https://en.wikipedia.org/wiki/Tachycardia
    :param age: age in integer
    :param heart_rate: person's heart rate in BPM ex(160)
    :return: True or False
    """
    if age < 1:
        if heart_rate > 169:
            return True
        else:
            return False
    elif age <= 2:
        if heart_rate > 151:
            return True
        else:
            return False
    elif age <= 4:
        if heart_rate > 137:
            return True
        else:
            return False
    elif age <= 7:
        if heart_rate > 133:
            return True
        else:
            return False
    elif age <= 11:
        if heart_rate > 130:
            return True
        else:
            return False
    elif age <= 15:
        if heart_rate > 119:
            return True
        else:
            return False
    elif age > 15:
        if heart_rate > 100:
            return True
        else:
            return False
