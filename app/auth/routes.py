from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from app.auth import functionality as func
from datetime import timedelta

bp_auth = Blueprint('bp_auth', __name__, url_prefix='/auth')

# Initialize JWT (this should be done in your app factory or main app file)
jwt = JWTManager()

# Example route to generate a token
@bp_auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Replace this with your actual authentication logic
    if func.authenticate_user(username, password):
        # Create a token with a 15-minute expiration
        access_token = create_access_token(identity=username, expires_delta=timedelta(minutes=15))
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Invalid username or password"}), 401

# Example protected route
@bp_auth.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200