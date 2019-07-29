import os

from flask import abort, Flask, jsonify, request
import googlemaps
import datetime
import logging
import json
import maps

app = Flask(__name__)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def is_request_valid(request):
    is_token_valid = request.form['token'] == os.environ['SLACK_VERIFICATION_TOKEN']
    print(request.form)
    return is_token_valid


@app.route('/travel-time', methods=['POST'])
def travel_time():
    print(request)
    if not is_request_valid(request):
        abort(400)
    msg = request.form['text']
    destinations = msg.split(';')
    try:
        t = maps.get_directions_duration(destinations[0].strip(), destinations[1].strip())
    except:
        return jsonify(
            response_type='in_channel',
            text='Invalid Address, Please re-enter.'
        )

    return jsonify(
        response_type='in_channel',
        text= t
    )

@app.route('/hello-there', methods=['POST'])
def hello_there():
    if not is_request_valid(request):
        abort(400)

    return jsonify(
        response_type='in_channel',
        text='Hello, I am a SlackBot!',
    )