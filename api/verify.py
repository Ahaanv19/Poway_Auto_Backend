from flask import Blueprint, request, jsonify, session
from flask_restful import Api, Resource

verify_api = Blueprint('verify', __name__, url_prefix='/api')
api = Api(verify_api)

entries = []

# Simulated user store
USERS = {
    'admin@site.com': {'name': 'Admin', 'role': 'Admin'},
    'user@site.com': {'name': 'User', 'role': 'User'}
}

class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get("email")

        if email not in USERS:
            return {"error": "Unauthorized"}, 401

        session['user'] = USERS[email] | {'email': email}
        return {"message": "Login successful", "user": session['user']}, 200

class EntryResource(Resource):
    def post(self):
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        address = data.get("address")

        user = session.get("user")
        if not user:
            return {"error": "Unauthorized"}, 401

        if user['role'] != 'Admin' and user['email'] != email:
            return {"error": "Users can only submit entries for themselves."}, 403

        if not all([name, email, address]):
            return {"error": "Missing fields"}, 400

        entries.append({"name": name, "email": email, "address": address})
        return {"message": "Entry added"}, 200

    def get(self):
        user = session.get("user")
        if not user:
            return {"error": "Unauthorized"}, 401

        if user['role'] != 'Admin':
            return {"error": "Only Admins can view all entries."}, 403

        return jsonify(entries)

api.add_resource(Login, '/login')
api.add_resource(EntryResource, '/entries')














