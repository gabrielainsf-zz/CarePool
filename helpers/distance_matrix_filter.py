"""
Send request to Google Distance Matrix API and filter results.

The function sends a request to the Google Distance Matrix API and filters
through the response to return possible drop-off locations under 45kms.
"""
import requests
from googlemaps import convert
from flask import json


def distance_matrix_filter(origin, destination, trips):
    """Return dictionary as trip_id: distance pairs."""
    trips_by_id = {trip.trip_id: trip for trip in trips}

    # Google Distance Matrix API set up
    base_url = ('https://maps.googleapis.com/maps/api/distancematrix/'
                'json?')
    payload = {
        "origins": convert.location_list(origin),
        "destinations": convert.location_list(destination),
        "units": "imperial"
    }

    r = requests.get(base_url, params=payload)

    drop_off_distances = {}

    if r.status_code != 200:
        print('HTTP status code {} received, program terminated.'
              .format(r.status_code))
    else:
        response_dict = json.loads(r.text)
        for offset, trip in enumerate(trips):
            cell = response_dict['rows'][0]['elements'][offset]
            if cell['status'] == 'OK':
                # Dictionary: key=trip_id, val=distance in meters
                drop_off_distances[trip.trip_id] = cell['distance']['value']
                # print('{} to {}: {}.'
                #       .format(src, dst, cell['distance']['text']))

    drop_off_distances = {key: value for key, value in drop_off_distances
                          .items() if value <= 72421}

    drop_offs_nearby = {}

    for trip_idx in drop_off_distances:
        trip = trips_by_id[trip_idx]
        drop_offs_nearby[trip_idx] = trip


    return drop_offs_nearby

def filter_by_distance():
    """Filter the results by distance and returns trips less than 45 miles."""


