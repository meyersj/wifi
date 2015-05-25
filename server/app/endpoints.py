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
    min_records = request.args.get("min_records")
    args = {}
    if location: args["location"] = location
    if age: args["age"] = int(age)
    if min_records: args["min_records"] = int(min_records)
    data = select.visits(**args)
    data["success"] = True
    return jsonify(data)

