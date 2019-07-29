import os
import datetime
import googlemaps


gmaps = googlemaps.Client(key=os.environ['GM_KEY'])

def get_directions_duration(address_dep, address_arriv):

    now = datetime.datetime.now()
    results = gmaps.directions(address_dep, address_arriv, mode="driving",departure_time=now)
    directions_result = results[0]['legs'][0]
    duration = directions_result['duration_in_traffic']
    t = f'Time to {address_arriv} : %s _(%s to %s)_' % (duration['text'], directions_result['start_address'],  directions_result['end_address'])
    return t
