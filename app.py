import os

from flask import abort, Flask, jsonify, request
import googlemaps
import datetime
import logging
import json

app = Flask(__name__)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def is_request_valid(request):
    is_token_valid = request.form['token'] == os.environ['SLACK_VERIFICATION_TOKEN']
    print(request.form)
    return is_token_valid


def get_directions_duration(address_dep, address_arriv, name_dest):
    """
    Get the duration in traffic using Google Maps API
    :param address_dep: departure address (as on Google Maps)
    :param address_arriv: arrival address
    :param name_dest: name of the destination
    :return: text with the ETA
    """
    # Connect to the API
    gmaps = googlemaps.Client(key=os.environ['GM_KEY'])
    now = datetime.datetime.now()
    # Compute the directions 
    results = gmaps.directions(address_dep, address_arriv, mode="driving",departure_time=now)
    directions_result = results[0]['legs'][0]
    # Get resukts
    duration = directions_result['duration_in_traffic']
    t = f'Time to {name_dest} : %s _(%s to %s)_' % (duration['text'], directions_result['start_address'],  directions_result['end_address'])
    return t


@app.route('/travel-time', methods=['POST'])
def travel_time():
    print(request)
    if not is_request_valid(request):
        abort(400)
    
    return jsonify(
        response_type='in_channel',
        text='Test Complete'
    )

@app.route('/hello-there', methods=['POST'])
def hello_there():
    if not is_request_valid(request):
        abort(400)

    return jsonify(
        response_type='in_channel',
        text='Hello, I am a SlackBot!',
    )