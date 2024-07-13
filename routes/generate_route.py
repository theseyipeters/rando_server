from flask import Blueprint, jsonify, request
from services.mock_data_service import generate_mock_data
from utils.provider_utils import choose_provider
from utils.auth_utils import token_required
from datetime import datetime
from extensions import mongo

generate_bp = Blueprint('generate_bp', __name__)

@generate_bp.route('/api/v1/generate', methods=['POST'])
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
        return jsonify({'data': mock_data, 'success':True , 'message': 'data generated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@generate_bp.route('/api/v1/generate-data', methods=['POST'])
@token_required
def generate_json_logged(user_id):
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
        
        # Log the activity
        activity_log = {
            'user_id': user_id,
            'activityType': "mock data generated",
            'activityTitle': "unsaved",
            'timestamp': datetime.utcnow(),
            'requested_data': data,
            'generated_data': mock_data  # You may choose to log only certain parts of the data
        }

        mock_data_generated = {
             'user_id': user_id,
             'data_name': 'unsaved',
             'template_name':"unsaved",
             'timestamp': datetime.utcnow(),
            'requested_data': data,
            'generated_data': mock_data 
        }
        mongo.db.user_activity.insert_one(activity_log)
        mongo.db.mock_data_generated.insert_one(mock_data_generated)
        
        return jsonify({'data': mock_data, 'success':True , 'message': 'data generated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


