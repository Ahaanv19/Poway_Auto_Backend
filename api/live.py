from flask import Blueprint, request, jsonify

incident_api = Blueprint('incident_api', __name__, url_prefix='/api')
incidents = []  # In-memory storage (replace with DB later)

@incident_api.route('/incidents', methods=['POST'])
def report_incident():
    data = request.get_json()
    if not data.get('location') or not data.get('type'):
        return jsonify({'error': 'Location and type are required'}), 400

    incidents.append({
        'location': data['location'],
        'type': data['type'],
        'details': data.get('details', '')
    })
    return jsonify({'message': 'Incident reported successfully'})

@incident_api.route('/incidents', methods=['GET'])
def get_incidents():
    return jsonify(incidents)

