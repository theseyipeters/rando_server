from flask import Blueprint, jsonify, request
from services.mock_data_service import generate_mock_data
from utils.provider_utils import choose_provider

generate_bp = Blueprint('generate_bp', __name__)

@generate_bp.route('/generate', methods=['POST'])
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
