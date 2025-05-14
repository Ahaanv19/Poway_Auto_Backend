from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
import requests
import re
from .traffic import get_average_speed

routes_api = Blueprint('routes', __name__, url_prefix='/api')
api = Api(routes_api)

API_KEY = 'AIzaSyDdw-OCP9d_GcwoVyX8EEWrdc4Mrz_D9ag'

def strip_html(text):
    return re.sub(r'<[^>]*>', '', text)

class RoutesAPI:
    class _GetRoutes(Resource):
        def post(self):
            data = request.get_json()
            origin = data.get('origin')
            destination = data.get('destination')
            mode = data.get('mode', 'driving')

            if not origin or not destination:
                return jsonify({'error': 'Origin and destination are required'}), 400

            url = (
                f"https://maps.googleapis.com/maps/api/directions/json?"
                f"origin={origin}&destination={destination}&alternatives=true"
                f"&mode={mode}&key={API_KEY}"
            )

            response = requests.get(url)
            data = response.json()

            if data['status'] == 'OK':
                routes = data['routes']
                route_info = []

                for route in routes:
                    steps = route['legs'][0]['steps']
                    route_details = []
                    total_duration_sec = 0

                    for step in steps:
                        instruction_html = step['html_instructions']
                        instruction = strip_html(instruction_html)
                        distance = step['distance']['text']
                        duration = step['duration']['text']
                        duration_val = step['duration']['value']

                        total_duration_sec += duration_val
                        route_details.append({
                            'instruction': instruction,
                            'distance': distance,
                            'duration': duration
                        })

                    total_duration_min = total_duration_sec / 60
                    adjusted = total_duration_min * 0.85  # Placeholder for dataset logic

                    route_info.append({
                        'details': route_details,
                        'total_duration': route['legs'][0]['duration']['text'],
                        'traffic_adjusted_duration': f"{adjusted:.1f} mins",
                        'total_distance': route['legs'][0]['distance']['text'],
                        'geometry': route['overview_polyline']['points']
                    })

                return jsonify(route_info)

            return jsonify({'error': data.get('status', 'No routes found')}), 500

    api.add_resource(_GetRoutes, '/get_routes')






