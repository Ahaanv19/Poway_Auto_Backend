from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
import requests

# Define Blueprint
routes_api = Blueprint('routes', __name__, url_prefix='/api')
api = Api(routes_api)

API_KEY = 'AIzaSyDdw-OCP9d_GcwoVyX8EEWrdc4Mrz_D9ag'

class RoutesAPI:
    class _GetRoutes(Resource):
        def post(self):
            data = request.get_json()
            origin = data.get('origin')
            destination = data.get('destination')
            mode = data.get('mode', 'driving')  # Default to driving if not provided

            if not origin or not destination:
                return jsonify({'error': 'Origin and destination are required'}), 400

            # Construct Google Maps API URL
            url = (
                f"https://maps.googleapis.com/maps/api/directions/json?"
                f"origin={origin}&destination={destination}&mode={mode}"
                f"&alternatives=true&key={API_KEY}"
            )

            response = requests.get(url)
            data = response.json()

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
                        'total_distance': route['legs'][0]['distance']['text'],
                        'geometry': route['overview_polyline']['points']
                    })

                return jsonify(route_info)

            return jsonify({'error': data.get('status', 'No routes found')}), 500

    api.add_resource(_GetRoutes, '/get_routes')
