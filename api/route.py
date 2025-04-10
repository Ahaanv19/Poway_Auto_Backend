from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from api.jwt_authorize import token_required
import requests

# Define Blueprint for modularizing the route API
routes_api = Blueprint('routes', __name__, url_prefix='/api')

# Attach RESTful API to the Blueprint
api = Api(routes_api)

# Google Maps API Key (replace with your key)
API_KEY = 'AIzaSyDdw-OCP9d_GcwoVyX8EEWrdc4Mrz_D9ag'

class RoutesAPI:
    """
    Define the API endpoint for retrieving routes using Google Maps Directions API.
    """

    class _GetRoutes(Resource):
        def post(self):
            # Parse request JSON
            data = request.get_json()
            origin = data.get('origin')
            destination = data.get('destination')

            # Validate inputs
            if not origin or not destination:
                return jsonify({'error': 'Origin and destination are required'}), 400

            # Construct Google Maps API URL
            url = (
                f"https://maps.googleapis.com/maps/api/directions/json?"
                f"origin={origin}&destination={destination}&alternatives=true&key={API_KEY}"
            )

            # Make request to Google Maps Directions API
            response = requests.get(url)
            data = response.json()

            # Process response
            if data['status'] == 'OK':
                routes = data['routes']
                route_info = []

                for route in routes:
                    steps = route['legs'][0]['steps']
                    route_details = []

                    for step in steps:
                        instruction = step['html_instructions']
                        distance = step['distance']['text']
                        duration = step['duration']['text']

                        route_details.append({
                            'instruction': instruction,
                            'distance': distance,
                            'duration': duration
                        })

                    route_info.append({
                        'details': route_details,
                        'total_duration': route['legs'][0]['duration']['text'],
                        'total_distance': route['legs'][0]['distance']['text']
                    })

                return jsonify(route_info)

            # Error case
            return jsonify({'error': data.get('status', 'No routes found')}), 500

    # Map the _GetRoutes class to the API endpoint
    api.add_resource(_GetRoutes, '/get_routes')
