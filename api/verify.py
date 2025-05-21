from flask import Blueprint, request, jsonify, session
from flask_restful import Api, Resource

verify_api = Blueprint('verify', __name__, url_prefix='/api')
api = Api(verify_api)

entries = []

class EntryResource(Resource):
    def post(self):
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        address = data.get("address")

        if not all([name, email, address]):
            return {"error": "Missing fields"}, 400

        entries.append({"name": name, "email": email, "address": address})
        return {"message": "Entry added"}, 200

    def get(self):
        # Backend role check (from session or user object)
        user = session.get("user")  # Assume user stored like: {"email": ..., "role": "admin"}
        if not user or user.get("role") != "admin":
            return {"error": "Access denied"}, 403

        return jsonify(entries)

api.add_resource(EntryResource, '/entries')



