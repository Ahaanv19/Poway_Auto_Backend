from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
import time

hazard_api = Blueprint('hazard_api', __name__, url_prefix='/api/hazard')
api = Api(hazard_api)

# In-memory hazard store (lat, lng, type, note, timestamp)
hazards = []

class HazardReportAPI:
    class _Post(Resource):
        def post(self):
            data = request.get_json()
            lat = data.get("latitude")
            lng = data.get("longitude")
            hazard_type = data.get("type")
            note = data.get("note", "")

            if not all([lat, lng, hazard_type]):
                return jsonify({'error': 'Missing fields'}), 400

            hazard = {
                "latitude": lat,
                "longitude": lng,
                "type": hazard_type,
                "note": note,
                "timestamp": time.time()
            }
            hazards.append(hazard)
            return jsonify({'message': 'Hazard reported successfully'})

    class _List(Resource):
        def get(self):
            # Auto-expire hazards older than 30 min
            now = time.time()
            fresh_hazards = [h for h in hazards if now - h["timestamp"] <= 1800]
            return jsonify(fresh_hazards)

    api.add_resource(_Post, '/report')
    api.add_resource(_List, '/all')
