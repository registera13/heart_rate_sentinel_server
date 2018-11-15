from flask import Flask, jsonify, request
from HRfunction import *
app = Flask(__name__)


@app.route("/api/new_patient", methods=["POST"])
def post_new_patient():
    p =  request.get_json()
    Patient(patient_id=p['patient_id'], attending_email=p['attending_email'], user_age=p['user_age']).save()
    return jsonify(p)

@app.route("/api/heart_rate", methods=["POST"])
def post_heart_rate():
    p = request.get_json()



@app.route("/api/status/patient", methods=["GET"])



@app.route("/api/heart_rate/<patient_id>", methods=["GET"])



@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])



@app.route("/api/heart_rate/interval_average", methods=["POST"])




if __name__ == "__main__":
    app.run(host="127.0.0.1")



















