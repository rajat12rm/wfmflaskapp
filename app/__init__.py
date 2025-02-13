from flask import Flask
from flask_cors import CORS
from .routes import init_routes
from config import Config
import logging
from .globals import init_app
from .routes.authentication import authentication_bp
from .routes.chat import chat_bp
logging.basicConfig(filename = 'systemlog.log',level=logging.DEBUG)

# def create_app():
#     app = Flask(__name__)
#     #handler = logging.FileHandler("test.log")
#     # Create the file logger
#     app.logger.addHandler(handler)             # Add it to the built-in logger
#     app.logger.setLevel(logging.DEBUG)         # Set the log level to debug
#     app.config.from_object(Config)
#     CORS(app)  # Enable CORS
#     init_routes(app)  # Initialize routes
#     return app

app=Flask(__name__)
CORS(app)
init_app(app)
app.config.from_object(Config)
app.register_blueprint(chat_bp)
app.register_blueprint(authentication_bp)