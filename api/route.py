from flask import Blueprint, request
from flask_restful import Api, Resource
import requests
import re
from .traffic import get_average_speed  # Optional: only if you're using real traffic data

# Blueprint and API init
routes_api = Blueprint('routes', __name__, url_prefix='/api')
api = Api(routes_api)

# Replace with your actual API key
API_KEY = 'AIzaSyC0qOeOkWMCMxT0bMAdpQzZesBsZ-zaFOM'

# Helper function to strip HTML tags from instructions
def strip_html(text):
    return re.sub(r'<[^>]*>', '', text)

class RoutesAPI:
    class _GetRoutes(Resource):
        def post(self):
            try:
                data = request.get_json()
                origin = data.get('origin')
                destination = data.get('destination')
                mode = data.get('mode', 'driving')

                if not origin or not destination:
                    return {'error': 'Origin and destination are required'}, 400

                # Request to Google Directions API
                url = (
                    f"https://maps.googleapis.com/maps/api/directions/json?"
                    f"origin={origin}&destination={destination}&alternatives=true"
                    f"&mode={mode}&key={API_KEY}"
                )

                response = requests.get(url)
                directions_data = response.json()

                # Handle failed directions response
                if directions_data.get('status') != 'OK':
                    return {'error': directions_data.get('status', 'Unknown error')}, 500

                routes = directions_data['routes']
                route_info = []

                for route in routes:
                    steps = route['legs'][0]['steps']
                    route_details = []
                    total_duration_sec = 0

                    for step in steps:
                        instruction = strip_html(step['html_instructions'])
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
                    adjusted = total_duration_min * 0.85  # Replace with dataset logic if needed

                    route_info.append({
                        'details': route_details,
                        'total_duration': route['legs'][0]['duration']['text'],
                        'traffic_adjusted_duration': f"{adjusted:.1f} mins",
                        'total_distance': route['legs'][0]['distance']['text'],
                        'geometry': route['overview_polyline']['points']
                    })

                # Return route data directly — Flask-RESTful auto-converts to JSON
                return route_info, 200

            except Exception as e:
                # Return error safely
                return {'error': str(e)}, 500

    # Route registration
    api.add_resource(_GetRoutes, '/get_routes')







