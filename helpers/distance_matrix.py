"""
Send request to Google Distance Matrix API and filter results.

The function sends a request to the Google Distance Matrix API and filters
through the response to return possible drop-off locations under 45kms.
"""
import requests
from googlemaps import convert
from flask import json


def distance_matrix(origin, destination):
    """Return dictionary as trip_id: distance pairs."""
    # Google Distance Matrix API set up
    base_url = ('https://maps.googleapis.com/maps/api/distancematrix/'
                'json?')
    payload = {
        "origins": convert.location_list(origin),
        "destinations": convert.location_list(destination),
        "units": "imperial"
    }

    r = requests.get(base_url, params=payload)

    distance_meters = None
    distance_miles = None

    if r.status_code != 200:
        print('HTTP status code {} received, program terminated.'
              .format(r.status_code))
    else:
        response_dict = json.loads(r.text)
        distance_meters = (response_dict['rows'][0]['elements'][0]['distance']
                           ['value'])
        distance_miles = (response_dict['rows'][0]['elements'][0]['distance']
                          ['text'])

    return (distance_meters, distance_miles)
