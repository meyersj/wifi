from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

app.debug = True

debug = app.logger.debug
error = app.logger.error

from app.mod_app.views import mod_app as app_module
from app.mod_sensor_api.endpoints import mod_sensor_api as sensor_api_module
from app.mod_web_api.endpoints import mod_web_api as web_api_module

app.register_blueprint(app_module)
app.register_blueprint(sensor_api_module)
app.register_blueprint(web_api_module)

