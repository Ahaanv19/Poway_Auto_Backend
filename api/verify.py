from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
import requests

verify_api = Blueprint('verify', __name__, url_prefix='/api')
api = Api(verify_api)

GOOGLE_API_KEY = 'AIzaSyDdw-OCP9d_GcwoVyX8EEWrdc4Mrz_D9ag'

class VerifyLocationAPI:
    class _Verify(Resource):
        def post(self):
            data = request.get_json()
            lat = data.get("latitude")
            lng = data.get("longitude")

            if lat is None or lng is None:
                return jsonify({'error': 'Coordinates required'}), 400

            url = (
                f"https://maps.googleapis.com/maps/api/geocode/json?"
                f"latlng={lat},{lng}&key={GOOGLE_API_KEY}"
            )

            try:
                res = requests.get(url)
                geodata = res.json()

                if geodata['status'] != 'OK':
                    return jsonify({'error': 'Failed to retrieve location'}), 400

                for component in geodata['results'][0]['address_components']:
                    if 'locality' in component['types']:
                        city = component['long_name']
                        if city.lower() == 'poway':
                            return jsonify({'valid': True, 'message': 'You are in Poway'})
                        break

                return jsonify({'valid': False, 'message': 'You are not in Poway'})

            except Exception as e:
                return jsonify({'error': str(e)}), 500

    api.add_resource(_Verify, '/verify_location')






