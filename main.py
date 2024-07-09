from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import mongo
from routes.auth_route import auth_bp
from routes.generate_route import generate_bp

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
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

if __name__ == '__main__':
    app.run(debug=True)
