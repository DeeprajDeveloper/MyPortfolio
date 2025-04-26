from typing import Union
from datetime import datetime
from flask import Blueprint, jsonify, request
from app.api import functionality as func

bp_api = Blueprint('bp_api', __name__, url_prefix='/api')
chat_log = []  # Temporary in-memory storage


@bp_api.route('/health', methods=['GET'])
def health():
    return jsonify({'apiStatus': 'healthy'})


@bp_api.route('/v1/get/exploreProjects', methods=['GET'])
def v1_explore_projects():
    filter_field: str = request.args.get('projectIdentifier')
    response_json = func.get_project_summary(filter_parameters=filter_field)
    return response_json


@bp_api.route('/v1/get/projectDetails', methods=['GET'])
def v1_project_details():
    filter_field: str = request.args.get('projectIdentifier')
    response_json = func.get_project_details(project_id=filter_field)
    return response_json


@bp_api.route('/v1/get/myInformation', methods=['GET'])
def v1_get_my_info():
    response_json: dict
    filter_field: str = request.args.get('filter')
    response_json = func.get_my_info(filter_parameters=filter_field)
    return response_json


@bp_api.route('/v1/update/myInformation', methods=['PUT'])
def v1_update_my_info():
    response_json: dict
    request_json: dict = request.get_json()
    response_json = func.update_my_info(json_input=request_json)
    return response_json


@bp_api.route('/v1/insert/basicProjectInformation', methods=['POST'])
def v1_insert_projects():
    response_json: dict
    request_json: dict = request.get_json()
    response_json = func.insert_projects(json_input=request_json)
    return response_json


@bp_api.route('/v1/message/add', methods=['POST'])
def v1_message_add():
    response_json: dict
    request_json: dict = request.get_json()
    response_json = func.add_message(json_input=request_json)
    return response_json


@bp_api.route('/v1/message/read', methods=['GET'])
def v1_message_read():
    response_json: dict
    filter_parameters: dict = request.get_json()
    response_json = func.read_message(filter_parameters=filter_parameters)
    return response_json


@bp_api.route('/v1/update/readMessage', methods=['PUT'])
def v1_message_update_status():
    response_json: dict
    message_id: Union[str, list] = request.args.get('messageIdentifier')
    if ',' in message_id:
        message_id = message_id.split(',')
    response_json = func.update_message_status(message_id)
    return response_json


@bp_api.route('/v1/chat/send', methods=['POST'])
def chat_send_message():
    data = request.get_json()
    response_data = func.process_chat(data, chat_log)
    return jsonify(chat_log)

