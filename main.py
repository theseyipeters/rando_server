from flask import Flask, Blueprint, jsonify, request
from flask_cors import CORS, cross_origin
from config import Config
from extensions import mongo
from routes.auth_route import auth_bp
from routes.generate_route import generate_bp
from routes.user_activity_route import user_activity_bp
from routes.mock_data_route import mock_data_bp
from routes.data_template_routes import data_template_bp

app = Flask(__name__)
app.config.from_object(Config)

# Configure CORS
CORS(app, resources={r"/*": {"origins": ["https://rando-webapp.vercel.app", "http://localhost:5000", "http://localhost:5173"]}})


mongo.init_app(app)

def test_mongo_connection():
    try:
        # Attempt to list collections in the database
        collections = mongo.db.list_collection_names()
        print(f"Successfully connected to MongoDB. Collections: {collections}")
    except Exception as e:
        print(f"Failed to connect to MongoDB. Error: {e}")

# Create indexes for username and email
with app.app_context():
    test_mongo_connection()
    mongo.db.users.create_index('username', unique=True)
    mongo.db.users.create_index('email', unique=True)

# Register blueprints (routes)
app.register_blueprint(auth_bp)
app.register_blueprint(generate_bp)
app.register_blueprint(user_activity_bp)
app.register_blueprint(mock_data_bp)
app.register_blueprint(data_template_bp)

# Example of adding CORS headers manually in a route
@app.after_request
def add_cors_headers(response):
    allowed_origins = ["https://rando-webapp.vercel.app", "http://localhost:5000", "http://localhost:5173"]
    origin = request.headers.get('Origin')
    if origin in allowed_origins:
        response.headers.add('Access-Control-Allow-Origin', origin)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


if __name__ == '__main__':
    app.run(debug=True)
