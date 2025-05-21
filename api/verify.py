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
        user = session.get("user")  # Expected: {"email": ..., "role": "Admin"}
        if not user or user.get("role", "").lower() != "admin":
            return {"error": "Access denied"}, 403

        return jsonify(entries)

# Optional: API to expose current user info for frontend role-based logic
class SessionInfo(Resource):
    def get(self):
        user = session.get("user")
        if not user:
            return {"error": "Not logged in"}, 401
        return {"email": user.get("email"), "role": user.get("role")}, 200

api.add_resource(EntryResource, '/entries')
api.add_resource(SessionInfo, '/userinfo')




