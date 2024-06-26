import os
from openai import OpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

client = OpenAI(
    api_key=os.environ.get('OPENAI_API_KEY')
)

@app.route('/generate-response', methods=['POST'])
def generate_response():
    data = request.json
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=data['messages'],
            temperature=data.get('temperature'),
            max_tokens=data.get('max_tokens'),
            top_p=data.get('top_p')
        )
        return response.choices[0].message.content, 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# This is a test API KEY with limited usage.
CARBON_API_KEY = os.environ.get('CARBON_API_KEY')

@app.route('/auth')
def auth_test():
    api_key = CARBON_API_KEY
    headers = {
        'Authorization': f'Bearer {api_key}',
    }
    response = requests.get("https://www.carboninterface.com/api/v1/auth", headers=headers)
    return response.json()

@app.route('/estimate/electricity', methods=['POST'])
def estimate_electricity():
    data = request.json
    response = requests.post(
        "https://www.carboninterface.com/api/v1/estimates",
        headers = {
            'Authorization': f'Bearer {CARBON_API_KEY}',
            'Content-Type': 'application/json',
        },
        json={
            "type": "electricity",
            "electricity_value": data.get("electricity_value"),
            "country": data.get("country"),
        }
    )
    return jsonify(response.json())

@app.route('/estimate/vehicle', methods=['POST'])
def estimate_vehicle():
    data = request.json
    response = requests.post(
        "https://www.carboninterface.com/api/v1/estimates",
        headers = {
            'Authorization': f'Bearer {CARBON_API_KEY}',
            'Content-Type': 'application/json',
        },
        json={
            "type": "vehicle",
            "distance_unit": data.get("distance_unit"),
            "distance_value": data.get("distance_value"),
            "vehicle_model_id": data.get("vehicle_model_id"),
        }
    )
    return jsonify(response.json())

@app.route('/estimate/fuel', methods=['POST'])
def estimate_fuel():
    data = request.json
    response = requests.post(
        "https://www.carboninterface.com/api/v1/estimates",
        headers = {
            'Authorization': f'Bearer {CARBON_API_KEY}',
            'Content-Type': 'application/json',
        },
        json={
            "type": "fuel_combustion",
            "fuel_source_type": data.get("fuel_source_type"),
            "fuel_source_unit": data.get("fuel_source_unit"),
            "fuel_source_value": data.get("fuel_source_value"),
        }
    )
    return jsonify(response.json())

@app.route('/estimate/shipping', methods=['POST'])
def estimate_shipping():
    data = request.json
    response = requests.post(
        "https://www.carboninterface.com/api/v1/estimates",
        headers = {
            'Authorization': f'Bearer {CARBON_API_KEY}',
            'Content-Type': 'application/json',
        },
        json={
            "type": "shipping",
            "weight_value": data.get("weight_value"),
            "weight_unit": data.get("weight_unit"),
            "distance_value": data.get("distance_value"),
            "distance_unit": data.get("distance_unit"),
            "transport_method": data.get("transport_method"),
        }
    )
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
