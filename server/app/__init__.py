from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
app.debug = True
debug = app.logger.debug
error = app.logger.error

from app import endpoints

