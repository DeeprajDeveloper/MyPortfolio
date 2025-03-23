from flask import Blueprint, jsonify, request
from app.api import functionality as func

bp_api = Blueprint('bp_api', __name__, url_prefix='/api')

