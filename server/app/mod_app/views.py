from flask import Blueprint, request, jsonify

from app import app, debug, error


mod_app = Blueprint('app', __name__, url_prefix='/')

@mod_app.route('/')
def index():
    return "root"


