from flask import Flask, request, jsonify
from functools import wraps
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from .config import Config
from dotenv import load_dotenv
from firebase_admin import credentials, initialize_app

import os

load_dotenv()

ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    CORS(app)
    config = Config()
    app.config.from_object(config)
    ma.init_app(app)
    root_dir = os.path.dirname(os.path.abspath(__file__))
    firebase_config_path = os.path.join(root_dir, 'caminante-db-firebase.json')
    cred = credentials.Certificate(firebase_config_path)
    initialize_app(cred)
    from src.routes.auth import auth_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    return app

