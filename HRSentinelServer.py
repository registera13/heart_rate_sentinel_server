from flask import Flask, jsonify, request
app = Flask(__name__)
from HRfunction import *

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


@app.route("/api/new_patient", methods=["POST"])
def post_patient():
    """
    Use create_patient input to create a the new patients
    the post the the data on to the data base
    :return:
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
    req_data = request.get_json()
    patient_id = req_data["patient_id"]
    heart_rate = req_data["heart_rate"]
    update_heart_rate(patient_id, heart_rate)
    return 200


@app.route("/api/status/<patient_id>", methods=["GET"])
def patient_status(patient_id):
    status=get_status(patient_id)
    print(status)
    return status, 200



@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def get_db_heart_rate(patient_id):
    hr=get_heart_rate(patient_id)
    print(hr)
    return jsonify(hr), 200


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def average_heart_rate(patient_id):
    hr = get_heart_rate(patient_id)
    avg_hr = cal_average_heart_rate(hr)
    return jsonify(avg_hr), 200

@app.route("/api/heart_rate/interval_average", methods=["POST"])




if __name__ == "__main__":
    app.run(host="127.0.0.1")



















