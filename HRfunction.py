import sendgrid
import os
from sendgrid.helpers.mail import *
import datetime
from flask import Flask, jsonify, request
from pymodm import connect
from pymodm import MongoModel, fields

connect("mongodb://GODUKE18:GODUKE18@ds039778.mlab.com:39778/bme590_sentinel_db")


class Patient(MongoModel):
    """
    Create MONGODB: ID, email, age, is tachycardic?, heart rate, and time.
    """
    patient_id = fields.CharField(primary_key=True)
    attending_email = fields.EmailField()
    user_age = fields.FloatField()
    is_tachycardic = fields.ListField(field=fields.BooleanField())
    heart_rate = fields.ListField(field=fields.IntegerField())
    heart_rate_time = fields.ListField(field=fields.DateTimeField())


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


def new_patient():
    """
    Use create_patient input to create a the new patients
    :return:
    """
    req_data = request.get_json()
    patient_id = req_data["patient_id"]
    attending_email = req_data["attending_email"]
    user_age = req_data["user_age"]
    create_patient(patient_id, attending_email, user_age)

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

def send_sendgrid():
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("test@example.com")
    to_email = Email("test@example.com")
    subject = "Sending with SendGrid is Fun"
    content = Content("text/plain", "and easy to do anywhere, even with Python")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)

if __name__ == "__main__":