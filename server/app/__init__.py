from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

app.debug = True

debug = app.logger.debug
error = app.logger.error

from app import endpoints

