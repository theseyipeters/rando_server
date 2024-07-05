from flask import Flask, jsonify, request
from flask_cors import CORS
from faker import Faker
from faker.providers import BaseProvider
import random
import re

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

# Initialize other providers
us_fake = Faker('en_US')

@app.route('/generate', methods=['POST'])
def generate_json():
    data = request.get_json()
    provider = request.args.get('provider')
    
    if not data or not provider:
        return jsonify({'error': 'Provider and template must be specified'}), 400

    try:
        # Check if top-level template is a list with repeat
        if isinstance(data, list) and len(data) == 2 and isinstance(data[0], str) and data[0].startswith('{{repeat('):
            mock_data = handle_repeat(data, provider)
        else:
            mock_data = generate_mock_data(data, provider)
        return jsonify(mock_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_mock_data(template, provider):
    mock_data = {}

    # Choose the appropriate provider
    fake_provider = choose_provider(provider)

    # First pass to ensure first_name and last_name are generated first
    for key, value in template.items():
        if isinstance(value, str) and (value.lower() == 'first_name' or value.lower() == 'firstname'):
            mock_data[key] = fake_provider.first_name()
        elif isinstance(value, str) and (value.lower() == 'last_name' or value.lower() == 'lastname'):
            mock_data[key] = fake_provider.last_name()

    # Second pass for other fields
    for key, value in template.items():
        if key not in mock_data:  # Skip already generated first_name and last_name
            if isinstance(value, dict):
                mock_data[key] = generate_mock_data(value, provider)
            elif isinstance(value, list):
                if isinstance(value[0], str) and value[0].startswith('{{repeat('):
                    mock_data[key] = handle_repeat(value, provider)
                elif all(isinstance(item, dict) for item in value):
                    mock_data[key] = [generate_mock_data(item, provider) for item in value]
                else:
                    mock_data[key] = fake_value(value, fake_provider)
            else:
                mock_data[key] = fake_value(value, fake_provider)
    
    # Ensure name is a combination of first_name and last_name if both are present
    first_name_keys = ['first_name', 'firstname']
    last_name_keys = ['last_name', 'lastname']
    
    first_name_value = None
    last_name_value = None
    
    for fn_key in first_name_keys:
        first_name_value = first_name_value or next((mock_data[key] for key in template if key.lower() == fn_key), None)
    
    for ln_key in last_name_keys:
        last_name_value = last_name_value or next((mock_data[key] for key in template if key.lower() == ln_key), None)

    if 'name' in template:
        first_name = first_name_value or fake_provider.first_name()
        last_name = last_name_value or fake_provider.last_name()
        mock_data['name'] = f"{first_name} {last_name}".strip()

    # Ensure email is generated based on first_name
    email_keys = ['email']
    for email_key in email_keys:
        if email_key in template:
            if first_name_value:
                first_name_for_email = first_name_value
            else:
                # Try to extract the first word from the 'name' field
                name_value = mock_data.get('name', '')
                first_name_for_email = name_value.split()[0] if name_value else fake_provider.first_name()
            mock_data['email'] = f"{first_name_for_email.lower()}@randotest.net"

    return mock_data

def handle_repeat(template, provider):
    # Extract the repeat count using regular expression
    repeat_str = template[0]
    match = re.match(r'{{repeat\((\d+)\)}}', repeat_str)
    if not match:
        raise ValueError(f"Invalid repeat format: {repeat_str}")
    repeat_count = int(match.group(1))
    item_template = template[1]

    return [generate_mock_data(item_template, provider) for _ in range(repeat_count)]

def choose_provider(provider):
    if provider == 'NG':
        return fake
    elif provider == 'US':
        return us_fake
    else:
        raise ValueError(f"Unsupported provider: {provider}")

def fake_value(value_type, fake_provider):
    if isinstance(value_type, str):
        value_type_lower = value_type.lower()
        if value_type_lower == 'name':
            return fake_provider.name()
        elif value_type_lower in ['first_name', 'firstname']:
            return fake_provider.first_name()
        elif value_type_lower in ['last_name', 'lastname']:
            return fake_provider.last_name()
        elif value_type_lower == 'address':
            return fake_provider.address()
        elif value_type_lower == 'email':
            return fake_provider.email()  # This will be overridden by the specific logic in generate_mock_data
        elif value_type_lower == 'phone_number':
            return fake_provider.phone_number()
        else:
            return None
    elif isinstance(value_type, list):
        return random.choice(value_type)
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)
