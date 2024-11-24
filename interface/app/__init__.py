# app/__init__.py

from flask import Flask
from flask_cors import CORS



def create_app():
    app = Flask(__name__)

    # Enable CORS for all routes
    CORS(app)

    from routes import guess_game
    app.register_blueprint(guess_game)

    return app
