from flask import Flask, make_response, jsonify
from flask_cors import CORS, cross_origin
import sqlite3

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Endpoint to fetch data
@app.route('/get-data', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_data():
    connection = sqlite3.connect('./tutorial.db')  # Path to your SQLite database
    cursor = connection.cursor()

    # Query data
    cursor.execute('SELECT * FROM DiabetesData')
    rows = cursor.fetchall()

    # # Return as JSON

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5055, debug=True)
