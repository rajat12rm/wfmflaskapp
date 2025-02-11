from flask import Flask
from .authentication import authentication_bp
from .chat import chat_bp

def init_routes(app: Flask):
    app.register_blueprint(authentication_bp)
    app.register_blueprint(chat_bp)
