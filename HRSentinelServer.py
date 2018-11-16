from HRfunction import *
from pymodm import connect
from pymodm import MongoModel, fields
from flask import Flask, jsonify, request
app = Flask(__name__)

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


@app.route("/api/new_patient", methods=["POST"])
def post_patient():
    """
    Webservice  that use create_patient input to create a the new patients
    the post the the data on to the data base
    :return: status code
    """
    req_data = request.get_json()
    patient_id = req_data["patient_id"]
    attending_email = req_data["attending_email"]
    user_age = req_data["user_age"]
    try:
        create_patient(patient_id, attending_email, user_age)
    except:
        return jsonify({"message": "Error occurred, check your inputs"}), 400
    return 200


@app.route("/api/heart_rate", methods=["POST"])
def post_heart_rate():
    """
    Webservice  that post heart rate to database based on the the patient id
    :return:status code
    """
    req_data = request.get_json()
    patient_id = req_data["patient_id"]
    heart_rate = req_data["heart_rate"]
    update_heart_rate(patient_id, heart_rate)
    return 200


@app.route("/api/status/<patient_id>", methods=["GET"])
def patient_status(patient_id):
    """
    Webservice to get the status of the patients status of the patients
    :param patient_id: patient id string
    :return: status dictionary, status code
    """
    status = get_status(patient_id)
    print(status)
    return status, 200


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def get_db_heart_rate(patient_id):
    """
    Webservice to get the patient's heart rate from database
    :param patient_id: patient id string
    :return: list of heart rate, status code
    """
    hr = get_heart_rate(patient_id)
    print(hr)
    return jsonify(hr), 200


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def average_heart_rate(patient_id):
    """
    Webservice to calculate the average heart rate of a patient using from data base
    :param patient_id: patient id string
    :return: average heart rate in json
    """
    hr = get_heart_rate(patient_id)
    avg_hr = cal_average_heart_rate(hr)
    return jsonify(avg_hr), 200


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def interval_average():
    """
    Webservice to calculate the average heart rate of a patient
    that is after a timestamp period using from data base.
    :return: average heart rate since interval in json
    """
    req_data = request.get_json()
    patient_id = req_data["patient_id"]
    heart_rate_average_since = req_data["heart_rate_average_since"]

    interval_timestamp = datetime.datetime.strptime(
        heart_rate_average_since, '%Y-%m-%d %H:%M:%S.%f')
    heart_rates = get_heart_rate(patient_id)
    p = Patient.objects.raw({"_id": patient_id}).first()
    heart_rate_times = p.heart_rate_time

    interval_avg_hr = get_interval_average_heart_rate(heart_rates,
                                                      heart_rate_times,
                                                      interval_timestamp)

    return jsonify(interval_avg_hr), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1")



















