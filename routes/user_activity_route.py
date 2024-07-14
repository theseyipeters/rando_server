# server/routes/user_activity_route.py

from flask import Blueprint, jsonify, request
from bson import ObjectId
from utils.auth_utils import token_required
from extensions import mongo

user_activity_bp = Blueprint('user_activity_bp', __name__)

@user_activity_bp.route('/api/v1/user-activities', methods=['GET'])
@token_required
def get_user_activities(user_id):
    try:
        activities = list(mongo.db.user_activity.find({'user_id': user_id}))
        for activity in activities:
            activity['_id'] = str(activity['_id'])  # Convert ObjectId to string for JSON serialization
        return jsonify({'data': activities, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_activity_bp.route('/api/v1/user-activities/<activity_id>', methods=['GET'])
@token_required
def get_user_activity(user_id, activity_id):
    try:
        activity = mongo.db.user_activity.find_one({'user_id': user_id, '_id': ObjectId(activity_id)})
        if activity:
            activity['_id'] = str(activity['_id'])  # Convert ObjectId to string for JSON serialization
            return jsonify({'data': activity, 'success': True})
        else:
            return jsonify({'error': 'Activity not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
