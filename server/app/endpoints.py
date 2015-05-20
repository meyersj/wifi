from flask import request

from app import app, debug, error
from processor import Processor


@app.route('/', methods=['GET'])
def index():
    return "root"


@app.route('/', methods=['POST'])
def data_stream():
    processor = Processor(data=request.data)
    return processor.run()


