import os

from flask import abort, Flask, jsonify, request
import datetime
import logging
import json
import maps
from addressDB import storeMapping, getMapping
import re

TAG_RE = re.compile(r'<[^>]+>')

app = Flask(__name__)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def remove_tags(text):
    return TAG_RE.sub('', text)

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
    for i in range(len(destinations)):
        destinations[i] = destinations[i].strip().lower()
    if len(destinations) != 2:
        return jsonify(
            repsonse_type='in_channel',
            text='Please enter starting address and end address.'
        )
    address1 = getMapping(request.form['user_id'], destinations[0])
    address2 = getMapping(request.form['user_id'], destinations[1])
    if type(address1) is str:
        destinations[0] = address1
    if type(address2) is str:
        destinations[1] = address2
    
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
    storeMapping(request.form['user_id'], mappings[1].strip().lower(), mappings[0].strip().lower())
    return jsonify(
        response_type='in_channel',
        text='{} can now be referred to as {}'.format(mappings[1], mappings[0])
    )
@app.route('/ping', methods=['POST'])
def response_data():
    return jsonify(
        response_type='in_channel',
        text='Server is up and running'
    )

@app.route('/get-mapping', methods=['POST'])
def get_mapper():
    msg = request.form['text']
    addresses = msg.strip().lower()
    response1 = getMapping(request.form['user_id'], addresses)
    print(response1)
    return jsonify(
        response_type='in_channel',
        text = response1
    )

@app.route('/directions', methods=['POST'])
def directions():
    if not is_request_valid(request):
        abort(400)
    msg = request.form['text']
    destinations = msg.split(';')
    for i in range(len(destinations)):
        destinations[i] = destinations[i].strip().lower()
    if len(destinations) != 2:
        return jsonify(
            repsonse_type='in_channel',
            text='Please enter starting address and end address.'
        )
    address1 = getMapping(request.form['user_id'], destinations[0])
    address2 = getMapping(request.form['user_id'], destinations[1])
    if type(address1) is str:
        destinations[0] = address1
    if type(address2) is str:
        destinations[1] = address2
    try:
        t = []
        travel_time = maps.get_directions_duration(destinations[0].strip(), destinations[1].strip())
        results = maps.get_directions(destinations[0].strip(), destinations[1].strip())
        t.append(travel_time)
        for i in results:
            t.append(remove_tags(i['html_instructions']))
        txt = '\n'.join(t)
        index = txt.index('Destination will be on')
        txt = txt[:index] + '\n' + txt[index:]
    except:
        return jsonify(
            response_type='in_channel',
            text='Invalid Address, Please re-enter.'
        )

    return jsonify(
        response_type='in_channel',
        text= txt
    )

@app.route('/geocode', methods=['POST'])
def geocode():
    if not is_request_valid(request):
        abort(400)
    msg = request.form['text']
    msg = msg.strip().lower()
    address1 = getMapping(request.form['user_id'], msg)
    if type(address1) is str:
        msg = address1
    try:
        location = maps.get_geocode(msg)
    except:
        return jsonify(
            response_type='in_channel',
            text='Invalid Address.'
        )
    return jsonify(
        response_type='in_channel',
        text= str(location)
    )