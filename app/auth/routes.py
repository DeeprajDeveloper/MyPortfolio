from flask import Blueprint, jsonify, request
from app.auth import functionality as func

bp_auth = Blueprint('bp_auth', __name__, url_prefix='/auth')
