# server/routes/mock_data_route.py

from flask import Blueprint, jsonify, request
from bson import ObjectId
from datetime import datetime
from utils.auth_utils import token_required
from extensions import mongo

mock_data_bp = Blueprint('mock_data_bp', __name__)

@mock_data_bp.route('/api/v1/mock-data', methods=['GET'])
@token_required
def get_mock_data(user_id):
    try:
        mock_data_list = list(mongo.db.mock_data_generated.find({'user_id': user_id}))
        for mock_data in mock_data_list:
            mock_data['_id'] = str(mock_data['_id'])  # Convert ObjectId to string for JSON serialization
        return jsonify({'mock_data': mock_data_list, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@mock_data_bp.route('/api/v1/mock-data/<data_id>', methods=['GET'])
@token_required
def get_single_mock_data(user_id, data_id):
    try:
        mock_data = mongo.db.mock_data_generated.find_one({'user_id': user_id, '_id': ObjectId(data_id)})
        if mock_data:
            mock_data['_id'] = str(mock_data['_id'])  # Convert ObjectId to string for JSON serialization
            return jsonify({'mock_data': mock_data, 'success': True})
        else:
            return jsonify({'error': 'Mock data not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@mock_data_bp.route('/api/v1/mock-data/<data_id>', methods=['PATCH'])
@token_required
def update_mock_data(user_id, data_id):
    data = request.get_json()
    data_name = data.get('data_name')
    template_name = data.get('template_name')
    save_as_template = data.get('save_as_template', False)
    
    if not data_name:
        return jsonify({'error': 'Data name is required'}), 400

    try:
        # Update the data_name and template_name
        update_data = {'data_name': data_name}
        if template_name:
            update_data['template_name'] = template_name
        
        update_result = mongo.db.mock_data_generated.update_one(
            {'user_id': user_id, '_id': ObjectId(data_id)},
            {'$set': update_data}
        )
        
        if update_result.modified_count == 0:
            return jsonify({'error': 'Mock data not found or no changes made'}), 404
        
        # Optionally save as a template
        if save_as_template:
            template = mongo.db.mock_data_generated.find_one({'_id': ObjectId(data_id)}, {'requested_data': 1, 'generated_data': 1})
            
            if template:
                new_template_id = ObjectId()  # Generate a new ObjectId for the template document
                new_template = {
                    '_id': new_template_id,
                    'template_name': template_name if template_name else data_name,  # Use template_name if provided, else data_name
                    'requested_data': template['requested_data'],  # Include requested_data in the template
                    'user_id': user_id,
                    'timestamp': datetime.utcnow(),
                }
                mongo.db.data_templates.insert_one(new_template)
        
        return jsonify({'message': 'Mock data updated successfully', 'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500