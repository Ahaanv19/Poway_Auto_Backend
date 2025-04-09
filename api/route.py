from flask import Blueprint, request, jsonify
import requests
from flask_cors import CORS

routes_bp = Blueprint('routes', __name__)
CORS(routes_bp, supports_credentials=True, methods=["GET", "POST", "OPTIONS"])


# Google Maps API Key (replace with your key)
API_KEY = 'AIzaSyDdw-OCP9d_GcwoVyX8EEWrdc4Mrz_D9ag'

@routes_bp.route('/get_routes', methods=['POST'])
def get_routes():
    data = request.json
    origin = data.get('origin')
    destination = data.get('destination')

    if not origin or not destination:
        return jsonify({'error': 'Origin and destination are required'}), 400

    url = (
        f"https://maps.googleapis.com/maps/api/directions/json?"
        f"origin={origin}&destination={destination}&alternatives=true&key={API_KEY}"
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
                'total_distance': route['legs'][0]['distance']['text']
            })

        return jsonify(route_info)

    return jsonify({'error': data.get('status', 'No routes found')}), 500