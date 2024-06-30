from flask import Flask, jsonify, request
from flask_cors import CORS
from faker import Faker
from faker.providers import BaseProvider
import json

# Import the data from separate files
from names import first_names, last_names
from streetsandcities import streets, cities

app = Flask(__name__)
CORS(app)

class NigeriaProvider(BaseProvider):
    def first_name(self):
        return self.random_element(first_names)

    def last_name(self):
        return self.random_element(last_names)
    
    def name(self):
        return f"{self.first_name()} {self.last_name()}"
    
    def phone_number(self):
        prefixes = ['070', '080', '090', '081']
        return f"{self.random_element(prefixes)}{self.numerify('########')}"
    
    def address(self):
        return f"{self.random_int(1, 100)} {self.random_element(streets)}, {self.random_element(cities)}"

fake = Faker('en_US')
fake.add_provider(NigeriaProvider)

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
    mock_data = {}

    # First pass to ensure first_name and last_name are generated first
    for key, value in data.items():
        if value == 'first_name':
            mock_data[key] = fake.first_name()
        elif value == 'last_name':
            mock_data[key] = fake.last_name()

    # Second pass for other fields
    for key, value in data.items():
        if key not in mock_data:  # Skip already generated first_name and last_name
            if isinstance(value, dict):
                mock_data[key] = generate_mock_data(value)
            elif isinstance(value, list):
                mock_data[key] = [generate_mock_data(item) for item in value]
            else:
                mock_data[key] = fake_value(value)
    
    # Ensure name is a combination of first_name and last_name if both are present
    if 'name' in data:
        first_name = mock_data.get('first_name', fake.first_name())
        last_name = mock_data.get('last_name', fake.last_name())
        mock_data['name'] = f"{first_name} {last_name}".strip()
    
    return mock_data

def fake_value(value_type):
    if value_type == 'name':
        return fake.name()
    elif value_type == 'first_name':
        return fake.first_name()  # Uses NigeriaProvider's first_name method
    elif value_type == 'last_name':
        return fake.last_name()   # Uses NigeriaProvider's last_name method
    elif value_type == 'address':
        return fake.address()
    elif value_type == 'email':
        return fake.email()
    elif value_type == 'phone_number':
        return fake.phone_number()
    # Add remaining cases here...
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)
