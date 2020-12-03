from flask import Flask
from flask_cors import CORS

from .webapp.master_routes import master_bp
from .webapp.user_routes import user_bp
from .webapp.device_api_routes import device_api_bp


app = Flask(__name__)
CORS(app)


app.register_blueprint(master_bp, url_prefix='/master')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(device_api_bp, url_prefix='/device-api')
