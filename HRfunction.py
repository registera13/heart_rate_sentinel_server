import sendgrid
import os
from sendgrid.helpers.mail import *
import datetime
from flask import Flask, jsonify, request


def create_patient(patient_id, attending_email, user_age):
    """
    create patient based on input
    :param patient_id: patient id NUM ex(1,2,3)
    :param attending_email: "example@duke.edu"
    :param user_age: age of the user
    :return:
    """
    p = Patient(patient_id=patient_id, attending_email=attending_email,
                user_age=user_age)
    p.save()
    return p

def update_heart_rate(patient_id, heart_rate):
    p = Patient.objects.raw({"_id": patient_id}).first()

    p.heart_rate.append(heart_rate)
    hr_timestamp = datetime.datetime.now()

    p.heart_rate_time.append(hr_timestamp)

    age = p.user_age
    tachycardic = is_tachycardic(age, heart_rate)
    if(tachycardic):
        attending_email = str(p.attending_email)
        try:
            send_tachycardic_email(patient_id, heart_rate, hr_timestamp,
                                   attending_email)
        except Exception:
            print("Please Configure Sendgrid API Key")

    p.is_tachycardic.append(tachycardic)
    p.save()


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

def send_email(patient_id, heart_rate, timestamp, attending_email):
    sg = sendgrid.SendGridAPIClient(apikey="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")
    from_email = Email("tachycardia_alert_server@bme590.com")
    to_email = Email(attending_email)
    subject = "Tachycardia alert for Patient ID " + str(patient_id)
    content = Content("text/plain",
                      "ALERT: Patient ID: " + patient_id + " was "
                      "tachycardic on " + timestamp.strftime("%B %d, %Y") + " at " + timestamp.strftime("%H:%M") + " with heart "
                      "rate of " + str(heart_rate) + " BPM.")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    #print(response.status_code)
    #print(response.body)
    #print(response.headers)
    return response.status_code

if __name__ == "__main__":