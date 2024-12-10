from flask import Flask, make_response, jsonify, request
from flask_cors import CORS, cross_origin
from sklearn.preprocessing import StandardScaler
import sqlite3
import numpy as np
import pandas as pd
from pickle import load

app = Flask(__name__)
CORS(app, supports_credentials=True)

scaler = StandardScaler()

cols_to_scale = ['BMI', 'GenHlth', 'MentHlth', 'PhysHlth', 'Age', 'Education', 'Income']

with open("model.pkl", "rb") as f:
    model = load(f)

with open("scaler.pkl", "rb") as f:
  scaler = load(f)


@app.route('/add-patient', methods=['POST'])
@cross_origin(supports_credentials=True)
def add_patient():
    input_data = request.json

    required_fields = [
        "PatientID", "Diabetes_binary", "HighBP", "HighChol", "CholCheck", "BMI", "Smoker",
        "Stroke", "HeartDiseaseorAttack", "PhysActivity", "Fruits", "Veggies",
        "HvyAlcoholConsump", "AnyHealthcare", "NoDocbcCost", "GenHlth",
        "MentHlth", "PhysHlth", "DiffWalk", "Sex", "Age", "Education", "Income"
    ]


    for field in required_fields:
        if field not in input_data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    try:
        connection = sqlite3.connect("tutorial.db")
        cursor = connection.cursor()

        # Insert the data into the database
        cursor.execute(
            "INSERT INTO DiabetesData (PatientID, Diabetes_binary, HighBP, HighChol, CholCheck, BMI, Smoker, Stroke, HeartDiseaseorAttack, PhysActivity, Fruits, Veggies, HvyAlcoholConsump, AnyHealthcare, NoDocbcCost, GenHlth, MentHlth, PhysHlth, DiffWalk, Sex, Age, Education, Income) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                input_data["PatientID"], input_data["Diabetes_binary"], input_data["HighBP"], input_data["HighChol"],
                input_data["CholCheck"], input_data["BMI"], input_data["Smoker"], input_data["Stroke"],
                input_data["HeartDiseaseorAttack"], input_data["PhysActivity"], input_data["Fruits"],
                input_data["Veggies"], input_data["HvyAlcoholConsump"], input_data["AnyHealthcare"],
                input_data["NoDocbcCost"], input_data["GenHlth"], input_data["MentHlth"], input_data["PhysHlth"],
                input_data["DiffWalk"], input_data["Sex"], input_data["Age"], input_data["Education"], input_data["Income"]
            )
        )

        connection.commit()
        connection.close()
        return jsonify({"message": "Patient added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-data', methods=['POST'])
@cross_origin(supports_credentials=True)
def get_data():
    connection = sqlite3.connect('./tutorial.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM DiabetesData')
    rows = cursor.fetchall()

    print(rows)

    data = [{'Diabetes_binary': row[0], 'HighBP': row[1], 'HighChol': row[2], 'CholCheck': row[3]} for row in rows]
    connection.close()
    return jsonify(data)

@app.route('/get-patient/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    connection = sqlite3.connect("tutorial.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM DiabetesData WHERE PatientID=?", (patient_id,))
    row = cursor.fetchone()
    connection.close()
    if row:
        return jsonify([dict(zip([column[0] for column in cursor.description], row))])
    else:
        return jsonify({"error": "Patient not found"}), 404

@app.route('/predict', methods=['POST'])
@cross_origin(supports_credentials=True)
def predict():
    input_data = request.json

    required_fields = [
        "HighBP", "HighChol", "CholCheck", "BMI", "Smoker",
        "Stroke", "HeartDiseaseorAttack", "PhysActivity", "Fruits", "Veggies",
        "HvyAlcoholConsump", "AnyHealthcare", "NoDocbcCost", "GenHlth",
        "MentHlth", "PhysHlth", "DiffWalk", "Sex", "Age", "Education", "Income"
    ]

    print(input_data)
    input_df = pd.DataFrame([input_data], columns=required_fields)
    print(input_df)
    input_df = input_df.astype(float)

    cols_to_scale = ['BMI', 'GenHlth', 'MentHlth', 'PhysHlth', 'Age', 'Education', 'Income']
    input_df[cols_to_scale] = scaler.transform(input_df[cols_to_scale])

    scaled_features = input_df.to_numpy()

    guess = model.predict(scaled_features)
    return jsonify({"probability": guess[0]})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5055, debug=True)
