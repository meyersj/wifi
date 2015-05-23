from flask import request, jsonify

from app import app, debug, error
from processor import Processor

from query import Select

@app.route('/', methods=['GET'])
def index():
    return "root"


@app.route('/', methods=['POST'])
def data_stream():
    processor = Processor(data=request.data)
    return processor.run()


@app.route('/recent', methods=['GET'])
def recent():
    select = Select()
    try:
        age = int(request.args.get("age"))
        location = request.args.get("location")
        data = select.recent_location(location=location, age=age)
        data["success"] = True
    except Exception:
        data["success"] = False
    return jsonify(data)


@app.route('/visits', methods=['GET'])
def visits():
    select = Select()
    try:
        age = int(request.args.get("age"))
        location = request.args.get("location")
        data = select.visits(location=location, age=age)
        data["success"] = True
    except Exception:
        data["success"] = False
    return jsonify(data)

