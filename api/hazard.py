from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource

hazards_api = Blueprint('hazards_api', __name__, url_prefix='/api')
api = Api(hazards_api)

# In-memory hazard store
hazard_store = []

class HazardAPI:
    class _Hazard(Resource):
        def get(self):
            return jsonify(hazard_store)

        def post(self):
            data = request.get_json()
            lat = data.get("latitude")
            lng = data.get("longitude")
            description = data.get("description")

            if not all([lat, lng, description]):
                return {"error": "Missing required fields"}, 400

            hazard = {
                "latitude": lat,
                "longitude": lng,
                "description": description
            }

            hazard_store.append(hazard)
            return jsonify({"message": "Hazard reported successfully"})

    api.add_resource(_Hazard, '/hazards')
