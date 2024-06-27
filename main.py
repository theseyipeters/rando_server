from flask import Flask, jsonify, request
from flask_cors import CORS
from faker import Faker
import json

app = Flask(__name__)
CORS(app)
fake = Faker()

# Endpoint to generate mock JSON data
@app.route('/generate', methods=['POST'])
def generate_json():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        # Generate mock data based on received JSON schema
        mock_data = generate_mock_data(data)
        return jsonify(mock_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_mock_data(data):
    # Function to generate mock data based on schema
    mock_data = {}
    for key, value in data.items():
        if isinstance(value, dict):
            mock_data[key] = generate_mock_data(value)
        elif isinstance(value, list):
            mock_data[key] = [generate_mock_data(item) for item in value]
        else:
            mock_data[key] = fake_value(value)
    return mock_data

def fake_value(value_type):
    # Generate fake data based on type
    if value_type == 'name':
        return fake.name()
    elif value_type == 'address':
        return fake.address()
    elif value_type == 'email':
        return fake.email()
    elif value_type == 'date':
        return fake.date()
    elif value_type == 'text':
        return fake.text()
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)
