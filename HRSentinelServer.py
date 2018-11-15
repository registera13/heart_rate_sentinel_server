from flask import Flask, jsonify, request
app = Flask(__name__)


@app.route("/api/new_patient", methods=["POST"])


@app.route("/api/heart_rate", methods=["POST"])



@app.route("/api/status/patient", methods=["GET"])



@app.route("/api/heart_rate/<patient_id>", methods=["GET"])



@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])



@app.route("/api/heart_rate/interval_average", methods=["POST"])




if __name__ == "__main__":
    app.run(host="127.0.0.1")



















