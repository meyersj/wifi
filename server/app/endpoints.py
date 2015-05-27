from flask import request, jsonify

from app import app, debug, error
from processor import Processor, Stream

from query import Select

@app.route('/', methods=['GET'])
def index():
    return "root"


@app.route('/', methods=['POST'])
def data_stream():
    processor = Processor(data=request.data)
    return processor.run()


@app.route('/stream', methods=['POST'])
def stream():
    stream = Stream(data=request.data)
    return stream.run()


@app.route('/visits', methods=['GET'])
def visits():
    select = Select()
    location = request.args.get("location")
    age = request.args.get("age")
    rate = request.args.get("rate")
    args = {}
    if location: args["location"] = location
    if age: args["age"] = int(age)
    if rate: args["rate"] = int(rate)
    data = select.visits(**args)
    data["success"] = True
    return jsonify(data)

@app.route('/visitor-history', methods=['GET'])
def visitor_history():
    select = Select()
    mac = request.args.get("mac")
    args = {}
    data = {"success":False}
    if mac:
        args["mac"] = mac
        data = select.visitor_history(**args)
        data["success"] = True
    return jsonify(data)

