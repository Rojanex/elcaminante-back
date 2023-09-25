from src.routes import auth_bp
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from .config import Config
from dotenv import load_dotenv
import pyrebase
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
    firebase_config_path = os.path.join(root_dir, 'firebase.json')
    cred = credentials.Certificate(firebase_config_path)
    initialize_app(cred)

    app.register_blueprint(auth_bp, url_prefix='/authentication')
    
    return app

