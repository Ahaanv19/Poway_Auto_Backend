# backend/live_traffic.py
from flask import Blueprint, request, jsonify

live_traffic_api = Blueprint('live_traffic', __name__, url_prefix='/api')
incidents = []  # In-memory storage

@live_traffic_api.route('/report_incident', methods=['POST'])
def report_incident():
    data = request.get_json()
    description = data.get("description")
    location = data.get("location")

    if not description or not location:
        return jsonify({"error": "Missing data"}), 400

    incidents.append({"description": description, "location": location})
    return jsonify({"message": "Incident reported successfully"}), 200

@live_traffic_api.route('/incidents', methods=['GET'])
def get_incidents():
    return jsonify(incidents), 200
