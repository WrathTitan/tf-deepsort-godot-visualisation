from flask import Flask, render_template
# import socket
import json
from data_stream import JSONStreamSubscriber

app = Flask(__name__)

hostname = "127.0.0.1"  # Use to receive from localhost
port = 5555
receiver = JSONStreamSubscriber(hostname, port)

@app.route('/')
def index():
    return {"server_status":"running","hello":"world"}

@app.route('/getbb')
def get_bounding_box():
    json_data = receiver.receive()
    print("JSON DATA: ",json_data)
    return json.loads(json_data)

if __name__=="__main__":
    app.run(debug=True)