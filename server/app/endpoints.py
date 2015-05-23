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
    print request.args
    mode = request.args["mode"]
    age = int(request.args.get("age"))
    data = {"success":False}
    if mode == "location":
        location = request.args.get("location")
        data = select.recent_location(location=location, age=age)
        data["success"] = True
    elif mode == "mac":
        mac = request.args.get("mac")
        data = select.recent_mac(mac=mac, age=age)
        data["success"] = True
    return jsonify(data)

