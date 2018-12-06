import sendgrid
import os
from sendgrid.helpers.mail import *
import datetime
from pymodm import connect
from pymodm import MongoModel, fields
connect("mongodb://GODUKE18:GODUKE18@ds039778.mlab.com:39778/bme590_sentinel_db")


class Patient(MongoModel):
    """
    Create MONGODB: ID, email, age, is tachycardic?, heart rate, and time.
    Patient_id:(str)
    attending_email:(str)
    user_age:(Float)
    is_tachycardic(Boolean list)
    heart_rate:(float list)
    heart_rate_time:(list datatimefield format)
    """
    patient_id = fields.CharField(primary_key=True)
    attending_email = fields.EmailField()
    user_age = fields.FloatField()
    is_tachycardic = fields.ListField(field=fields.BooleanField())
    heart_rate = fields.ListField(field=fields.FloatField())
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


def update_heart_rate(patient_id, heart_rate):
    """
    Create timestamp using the following methods
    https://stackoverflow.com/questions/13890935/does-pythons-time-time-return-the-local-or-utc-timestamp
    :param patient_id: patient id NUM ex(1,2,3)
    :param heart_rate: float
    :return:
    """
    p = Patient.objects.raw({"_id": patient_id}).first()

    p.heart_rate.append(heart_rate)
    hr_timestamp = datetime.datetime.now()

    p.heart_rate_time.append(hr_timestamp)

    patient_age = p.user_age
    tachycardic = is_tachycardic(patient_age, heart_rate)
    if tachycardic:
        attending_email = str(p.attending_email)
        try:
            send_email(patient_id, heart_rate, hr_timestamp,
                       attending_email)
        except Exception:
            print("Sendgrid error check api key and make sure it is installed")
    p.is_tachycardic.append(tachycardic)
    p.save()


def get_heart_rate(patient_id):
    """
    Get heart rate list from DB
    :param patient_id: patient id NUM ex(1,2,3)
    :return: heart rate in list
    """
    r = Patient.objects.raw({"_id": patient_id}).first()
    heart_rates = r.heart_rate
    return heart_rates


def cal_average_heart_rate(heart_rate):
    """
    Calculate the mean/average of the heart rate list
    :param heart_rate: list of heart rates
    :return: avg HR float
    """
    avg_hr = sum(heart_rate)/len(heart_rate)
    return avg_hr


def get_status(patient_id):
    """
    get the status of the patients based on his/her heart rate and age, and
    status will be if he/her is tachyardic or not
    :param patient_id: patient id NUM ex(1,2,3)
    :return: True or False for tachycardic then the timestamp
    """
    try:
        p = Patient.objects.raw({"_id": patient_id}).first()
        output_dict = {}
        output_dict["is_tachycardic"] = p.is_tachycardic[-1]
        output_dict["timestamp"] = p.heart_rate_time[-1]
        return output_dict
    except:
        print("Invalid patient ID")
        logging.error("Invalid patient ID.")


def get_interval_average_heart_rate(heart_rates, heart_rate_times, heart_rate_average_since):
    """
    Find the average heart rate from a given time interval in timestamp
    :param heart_rates: float heart rate
    :param heart_rate_times: timestamp
    :param heart_rate_average_since: timestamp from jason
    :return: float avg heart rate of the given interval
    """
    index_list = [index for index, time in enumerate(heart_rate_times) if time >= heart_rate_average_since]
    heart_rates_interval = [heart_rates[i] for i in index_list]
    hr_int_avg = sum(heart_rates_interval)/len(heart_rates_interval)
    return hr_int_avg


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
    """
    Send email using sendgrid server
    :param patient_id: str
    :param heart_rate: float
    :param timestamp: str, Date/time ex(2012-12-15 11:15:24.984000)
    :param attending_email: 'example@duke.edu'
    :return: status code
    """
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("tachycardia_alert_server@bme590.com")
    to_email = Email(attending_email)
    subject = "Tachycardia alert for Patient ID " + str(patient_id)
    content = Content("text/plain",
                      "ALERT: Patient ID: " + patient_id + " was "
                      "tachycardic on " + timestamp.strftime("%B %d, %Y") + " at " + timestamp.strftime("%H:%M") +
                      " with heart rate: " + str(heart_rate) + " BPM.")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    # print(response.status_code)
    # print(response.body)
    # print(response.headers)
    return response.status_code
