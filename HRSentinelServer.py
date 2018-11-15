from flask import Flask, jsonify, request
from HRfunction import *
app = Flask(__name__)


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
    create_patient(patient_id, attending_email, user_age)




@app.route("/api/heart_rate", methods=["POST"])
def post_heart_rate():
    p = request.get_json()



@app.route("/api/status/patient", methods=["GET"])



@app.route("/api/heart_rate/<patient_id>", methods=["GET"])



@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])



@app.route("/api/heart_rate/interval_average", methods=["POST"])




if __name__ == "__main__":
    app.run(host="127.0.0.1")



















