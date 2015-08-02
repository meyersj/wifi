from flask import Blueprint, request, jsonify, render_template

from app import app, debug, error


mod_app = Blueprint('app', __name__, url_prefix='/app')

@mod_app.route('/test')
def index():
    return "app root"
    

@mod_app.route('/devices')
def devices():
    return render_template("devices.html")


