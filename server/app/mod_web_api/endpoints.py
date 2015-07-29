from flask import Blueprint, request, jsonify

from app import app, debug, error


mod_web_api = Blueprint('web_api', __name__, url_prefix='/api')

@mod_web_api.route('/')
def api_index():
    return "api root"


