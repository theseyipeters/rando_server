
from flask import Blueprint, jsonify, request
from utils.auth_utils import token_required
from extensions import mongo
from bson import ObjectId  # Import ObjectId for working with MongoDB ObjectId

data_template_bp = Blueprint('data_template_bp', __name__)

@data_template_bp.route('/api/v1/templates', methods=['GET'])
@token_required
def get_all_templates(user_id):
    try:
        templates = list(mongo.db.data_templates.find({'user_id': user_id}, {'_id': 1, 'template_name': 1, 'timestamp': 1, 'requested_data':1}))
        
        for template in templates:
            template['_id'] = str(template['_id'])  # Convert ObjectId to string for JSON serialization
        
        return jsonify({'data': templates, 'success': True, 'message': 'Templates fetched successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@data_template_bp.route('/api/v1/templates/<template_id>', methods=['GET'])
@token_required
def get_template(user_id, template_id):
    try:
        # Convert template_id to ObjectId
        obj_id = ObjectId(template_id)
        template = mongo.db.data_templates.find_one({'user_id': user_id, '_id': obj_id}, {'_id': 1, 'template_name': 1, 'timestamp': 1})
        
        if not template:
            return jsonify({'error': 'Template not found'}), 404
        
        template['_id'] = str(template['_id'])  # Convert ObjectId to string for JSON serialization
        
        return jsonify({'data': template, 'success': True, 'message': 'Template fetched successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


