from flask import Blueprint, request, jsonify

from app import app, debug, error
from request_processor import Processor


mod_sensor_api = Blueprint('sensor_api', __name__, url_prefix='/sensor')


@mod_sensor_api.route('/')
def sensor_index():
    return "sensor index"


@mod_sensor_api.route('/data', methods=['post'])
def data_stream():
    processor = Processor(data=request.data)
    response = processor.run()
    return response


