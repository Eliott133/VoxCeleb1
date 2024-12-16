from flask import Flask
from app.routes.filters import filters_bp
from app.routes.audio import audio_bp
from app.extensions import socketio

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'

    app.register_blueprint(filters_bp)
    app.register_blueprint(audio_bp)

    socketio.init_app(app)  # Initialisation de SocketIO avec Flask
    return app
