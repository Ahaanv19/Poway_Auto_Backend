from flask import Blueprint, request, jsonify
import requests
import pandas as pd

routes_bp = Blueprint('routes', __name__)

# Load traffic data
def load_traffic_data():
    df = pd.read_csv('traffic_counts_datasd.csv')
    df['date_count'] = pd.to_datetime(df['date_count'])
    traffic_by_street = df.groupby('street_name')['total_count'].mean().to_dict()
    return traffic_by_street

API_KEY = 'AIzaSyDdw-OCP9d_GcwoVyX8EEWrdc4Mrz_D9ag'

@routes_bp.route('/get_routes', methods=['POST'])
def get_route_with_traffic():
    data = request.json
    origin = data.get('origin')
    destination = data.get('destination')
    traffic_data = load_traffic_data()

    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&alternatives=true&key={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':
        routes = data['routes']
        route_info = []

        for route in routes:
            steps = route['legs'][0]['steps']
            route_traffic_score = 0
            route_details = []

            for step in steps:
                instruction = step['html_instructions']
                distance = step['distance']['text']
                duration = step['duration']['text']

                street_name = None
                if 'onto' in instruction:
                    street_name = instruction.split('onto')[-1].split('<')[0].strip()

                traffic_count = 0
                if street_name:
                    for known_street in traffic_data:
                        if street_name.upper() in known_street:
                            traffic_count = traffic_data[known_street]
                            break

                route_traffic_score += traffic_count

                route_details.append({
                    'instruction': instruction,
                    'distance': distance,
                    'duration': duration,
                    'traffic_count': traffic_count
                })

            route_info.append({
                'traffic_score': route_traffic_score,
                'details': route_details,
                'total_duration': route['legs'][0]['duration']['text'],
                'total_distance': route['legs'][0]['distance']['text']
            })

        route_info.sort(key=lambda x: x['traffic_score'])
        return jsonify(route_info)

    return jsonify({'error': 'No routes found'})
