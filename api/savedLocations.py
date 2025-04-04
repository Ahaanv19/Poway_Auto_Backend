from flask import Blueprint, request
from flask_restful import Api, Resource
from model.savedLocations import db, SavedLocation

# Blueprint setup for the API
savedlocation_api = Blueprint('savedlocation_api', __name__, url_prefix='/api')
api = Api(savedlocation_api)

class SavedLocationListAPI(Resource):
    """Handles GET (list all) and POST (add new location)"""

    def get(self):
        saved_locations = SavedLocation.query.all()
        return {"locations": [location.read() for location in saved_locations]}, 200

    def post(self):
        data = request.get_json()
        if not data or 'name' not in data:
            return {'error': 'Location name is required.'}, 400

        existing_location = SavedLocation.query.filter_by(name=data['name']).first()
        if existing_location:
            return {'error': 'Location with this name already exists.'}, 400

        new_location = SavedLocation(name=data['name'])
        db.session.add(new_location)
        db.session.commit()

        return new_location.read(), 201

class SavedLocationDetailAPI(Resource):
    """Handles PUT (update) and DELETE (remove)"""

    def put(self, location_id):
        data = request.get_json()
        if not data or 'name' not in data:
            return {'error': 'Location name is required.'}, 400

        location = SavedLocation.query.get(location_id)
        if not location:
            return {'error': 'Location not found.'}, 404

        location.name = data['name']
        db.session.commit()

        return location.read(), 200

    def delete(self, location_id):
        location = SavedLocation.query.get(location_id)
        if not location:
            return {'error': 'Location not found.'}, 404

        db.session.delete(location)
        db.session.commit()

        return {'message': 'Location deleted successfully.'}, 200

# Add the resources to the API with proper routes
api.add_resource(SavedLocationListAPI, '/saved_locations')
api.add_resource(SavedLocationDetailAPI, '/saved_locations/<int:location_id>')
