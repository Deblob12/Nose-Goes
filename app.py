import os

from flask import abort, Flask, jsonify, request
import datetime
import logging
import json
import maps
from addressDB import storeMapping

app = Flask(__name__)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def is_request_valid(request):
    is_token_valid = request.form['token'] == os.environ['SLACK_VERIFICATION_TOKEN']
    return is_token_valid


@app.route('/travel-time', methods=['POST'])
def travel_time():
    print(request)
    if not is_request_valid(request):
        abort(400)
    msg = request.form['text']
    destinations = msg.split(';')
    if len(destinations) != 2:
        return jsonify(
            repsonse_type='in_channel',
            text='Please enter starting address and end address.'
        )
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

@app.route('/save', methods=['POST'])
def save():
    if not is_request_valid(request):
        abort(400)
    msg = request.form['text']
    mappings = msg.split(';')
    if len(mappings) != 2:
        return jsonify(
            repsonse_type='in_channel',
            text='Please enter nickname and address.'
        )
    storeMapping(request.form['user_id'], mappings[0], mappings[1])
    return jsonify(
        response_type='in_channel',
        text='{} can now be referred to as {}'.format(mappings[0], mappings[1])
    )
@app.route('/ping', methods=['POST'])
def response_data():
    return jsonify(
        response_type='in_channel',
        text='Server is up and running'
    )