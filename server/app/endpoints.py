from flask import request, jsonify

from app import app, debug, error
from request_processor import Processor



@app.route('/', methods=['GET'])
def index():
    return "root"

@app.route('/data', methods=['POST'])
def data_stream():
    processor = Processor(data=request.data)
    response = processor.run()
    return response


