import config
from datetime import datetime
from typing import Union, List
from app.constants import (QueryString as Query, ResponseKeysList as Keys, ValidIdentifiers as ValidIds, Mapping as Map)
from utils import (custom_error as err, db_util as db, build_json_response as build)


def get_project_summary(filter_parameters: Union[str, list]):
    database_name: str = config.DATABASE_URL

    project_summary: list
    project_ids: list
    project_techstack: list = []
    result_json: List[dict] = []
    project_element: dict = {}

    try:

        if filter_parameters in [None, '']:
            project_ids = db.dql_fetch_all_rows(database=database_name, sql_script=Query.PROJECT_ALL_IDS, return_list=False)
            if len(project_ids) > 1:
                for project_id in project_ids:
                    project_summary = db.dql_fetch_all_rows_for_one_input(database=database_name, sql_script=Query.PROJECT_SUMMARY_BY_ID, data_input=project_id[0], return_list=False)[0]
                    project_techstack = db.dql_fetch_all_rows_for_one_input(database=database_name, sql_script=Query.PROJECT_TECH_STACK, data_input=project_id[0], return_list=True)
                    project_element = {
                        "projectIdentifier": project_id[0],
                        "projectName": project_summary[0],
                        "projectSummary": project_summary[1],
                        "technologyStackList": project_techstack,
                        "displayImageLocation": project_summary[2],
                        "isActive": True if project_summary[3] == 1 else False
                    }
                    result_json.append(project_element)
        elif type(filter_parameters) is list:
            for project_id in filter_parameters:
                project_summary = db.dql_fetch_all_rows_for_one_input(database=database_name, sql_script=Query.PROJECT_SUMMARY_BY_ID, data_input=project_id, return_list=False)[0]
                project_techstack = db.dql_fetch_all_rows_for_one_input(database=database_name, sql_script=Query.PROJECT_TECH_STACK, data_input=project_id, return_list=True)
                project_element = {
                    "projectIdentifier": project_id,
                    "projectName": project_summary[0],
                    "projectSummary": project_summary[1],
                    "technologyStackList": project_techstack,
                    "displayImageLocation": project_summary[2],
                    "isActive": True if project_summary[3] == 1 else False
                }
                result_json.append(project_element)
        else:
            project_summary = db.dql_fetch_all_rows_for_one_input(database=database_name, sql_script=Query.PROJECT_SUMMARY_BY_ID, data_input=filter_parameters, return_list=False)[0]
            project_techstack = db.dql_fetch_all_rows_for_one_input(database=database_name, sql_script=Query.PROJECT_TECH_STACK, data_input=filter_parameters, return_list=True)
            project_element = {
                "projectIdentifier": filter_parameters,
                "projectName": project_summary[0],
                "projectSummary": project_summary[1],
                "technologyStackList": project_techstack,
                "displayImageLocation": project_summary[2],
                "isActive": True if project_summary[3] == 1 else False
            }
            result_json.append(project_element)

        return result_json
    except Exception as error:
        raise error


def get_project_details(project_id: str):
    database_name: str = config.DATABASE_URL

    project_summary: list
    project_ids: list
    project_techstack: list = []
    result_json: dict = {}
    project_element: dict = {}

    try:
        if project_id is not None:
            project_summary = db.dql_fetch_all_rows_for_one_input(database=database_name, sql_script=Query.PROJECT_SUMMARY_BY_ID, data_input=project_id, return_list=False)[0]
            project_details = db.dql_fetch_all_rows_for_one_input(database=database_name, sql_script=Query.PROJECT_DETAILS_BY_ID, data_input=project_id, return_list=False)[0]
            project_techstack = db.dql_fetch_all_rows_for_one_input(database=database_name, sql_script=Query.PROJECT_TECH_STACK, data_input=project_id, return_list=True)
            project_element = {
                "projectIdentifier": project_id,
                "projectName": project_summary[0],
                "projectSummary": project_summary[1],
                "technologyStackList": project_techstack,
                "displayImageLocation": project_summary[2],
                "projectOverview": project_details[0],
                "problemStatement": project_details[1],
                "solutionApproach": project_details[2],
                "hasProjectPreview": True if project_details[3] == 1 else False,
                "hasProjectGithubRepository": True if project_details[4] == 1 else False,
                "links": {
                    "githubRepository": project_details[5],
                    "projectPreview": project_details[6]
                },
                "isActive": True if project_summary[3] == 1 else False
            }
            result_json = project_element
        else:
            raise err.NoContent(message='Project ID provided does not exist.')

        return result_json
    except Exception as error:
        return build.response_template(success=False, display_error=True, error=error, status_code=400, message="An error has occurred. Please refer the errorInformation section for details.")


def get_my_info(filter_parameters: str = None) -> dict:
    database_name: str = config.DATABASE_URL
    sql_query_list: list
    result_json: dict = {}
    response_json: dict

    banner_info: list
    about_me: str
    top_display: str
    expertise: list
    experience: list
    try:
        banner_info = db.dql_fetch_all_rows_for_one_input(database=database_name, sql_script=Query.GENERAL_DATAVALUE_BY_KEY, data_input='displayBannerTechnologyStack', return_list=True)
        about_me = db.dql_fetch_all_rows_for_one_input(database=database_name, sql_script=Query.GENERAL_DATAVALUE_BY_KEY, data_input='aboutMe', return_list=True)[0]
        top_display = db.dql_fetch_all_rows_for_one_input(database=database_name, sql_script=Query.GENERAL_DATAVALUE_BY_KEY, data_input='topDisplayProjectIdentifiers', return_list=True)[0]
        expertise = db.dql_fetch_all_rows(database=database_name, sql_script=Query.EXPERTISE_LIST, return_list=False)
        experience = db.dql_fetch_all_rows(database=database_name, sql_script=Query.EXPERIENCE_LIST, return_list=False)

        result_json = {
            "myInformation": {
                "displayBannerTechnologyStacks": banner_info,
                "aboutMe": about_me,
                "topDisplayProjectIdentifiers": top_display,
                "myIndustryExperiences": build.json_builder_from_list(keys_list=Keys.EXPERIENCE_KEYS, data_list=experience, return_type='list'),
                "myExpertise": build.json_builder_from_list(keys_list=Keys.EXPERTISE_KEYS, data_list=expertise, return_type='list')
            }
        }

        response_json = result_json['myInformation'][filter_parameters] if filter_parameters is not None else result_json
        return response_json
    except Exception as error:
        return build.response_template(success=False, display_error=True, error=error, status_code=400, message="An error has occurred. Please refer the errorInformation section for details.")


def update_my_info(json_input: dict) -> dict:
    data_extract: dict
    result_json: dict
    old_value: str
    new_value: str
    database_name: str = config.DATABASE_URL
    sql_query: str
    keys_list: list = []

    try:
        if 'U' in json_input['action']:
            update_payload: Union[dict, list] = json_input['dataInput']
            if len(update_payload) > 0:
                for update_item in update_payload:
                    for key, value in update_item.items():
                        keys_list.append(key)
                    if keys_list == ValidIds.UPDATE_PAYLOAD_KEYS:
                        _perform_update(payload=update_item, database_name=database_name)
                    else:
                        raise err.InvalidPayload(message=f'Payload is missing certain parameters. Payload must contain {ValidIds.UPDATE_PAYLOAD_KEYS}. Please revalidate the payload and retry the operation.')
            else:
                for key, value in update_payload.items():
                    keys_list.append(key)
                if keys_list == ValidIds.UPDATE_PAYLOAD_KEYS:
                    _perform_update(payload=update_payload[0], database_name=database_name)
                else:
                    raise err.InvalidPayload(message=f'Payload is missing certain parameters. Payload must contain {ValidIds.UPDATE_PAYLOAD_KEYS}. Please revalidate the payload and retry the operation.')

        elif json_input['action'] in ValidIds.OPERATIONS and json_input['action'] != 'U':
            raise err.InvalidAction(message=f'Action {json_input["action"]} not allowed for this api endpoint.')
        else:
            raise err.InvalidOperation(message=f"Operation {json_input['action']} provided is invalid")

        return build.response_template(success=True, display_error=False, status_code=200, message="Operation completed successfully.")
    except Exception as error:
        return build.response_template(success=False, display_error=True, error=error, status_code=400, message="An error has occurred. Please refer the errorInformation section for details.")


def insert_projects(json_input: dict) -> dict:
    data_extract: dict
    result_json: dict
    database_name: str = config.DATABASE_URL
    sql_query: str
    keys_list: list = []

    try:
        if 'I' in json_input['action']:
            insert_payload: Union[dict, list] = json_input['dataInput']
            if len(insert_payload) > 0:
                for insert_item in insert_payload:
                    for key, value in insert_item.items():
                        keys_list.append(key)
                    if keys_list == ValidIds.INSERT_PAYLOAD_PROJECT_KEYS:
                        _perform_insert_project(payload=insert_item, database_name=database_name)
                    else:
                        raise err.InvalidPayload(message=f'Payload is missing certain parameters. Payload must contain {ValidIds.UPDATE_PAYLOAD_KEYS}. Please revalidate the payload and retry the operation.')
            else:
                for key, value in insert_payload.items():
                    keys_list.append(key)
                if keys_list == ValidIds.INSERT_PAYLOAD_PROJECT_KEYS:
                    _perform_insert_project(payload=insert_payload[0], database_name=database_name)
                else:
                    raise err.InvalidPayload(message=f'Payload is missing certain parameters. Payload must contain {ValidIds.UPDATE_PAYLOAD_KEYS}. Please revalidate the payload and retry the operation.')

        elif json_input['action'] in ValidIds.OPERATIONS and json_input['action'] != 'I':
            raise err.InvalidAction(message=f'Action {json_input["action"]} not allowed for this api endpoint.')
        else:
            raise err.InvalidOperation(message=f"Operation {json_input['action']} provided is invalid")

        return build.response_template(success=True, display_error=False, status_code=200, message="Operation completed successfully.")
    except Exception as error:
        return build.response_template(success=False, display_error=True, error=error, status_code=400, message="An error has occurred. Please refer the errorInformation section for details.")


def add_message(json_input: dict):
    database_name: str = config.DATABASE_URL
    sql_query_list: list
    result_json: dict = {}
    response_json: dict
    keys_list: list = []
    try:
        for key, value in json_input.items():
            keys_list.append(key)
        if keys_list == ValidIds.INSERT_PAYLOAD_MESSAGE_KEYS:
            _perform_insert_message(payload=json_input, database_name=database_name)
            return build.response_template(success=True, display_error=False, status_code=200, message="Operation completed successfully.")
        else:
            raise err.InvalidPayload(message=f'Payload is missing certain parameters. Payload must contain {ValidIds.INSERT_PAYLOAD_MESSAGE_KEYS}. Please revalidate the payload and retry the operation.')
    except Exception as error:
        raise build.response_template(success=False, display_error=True, error=error, status_code=400, message="An error has occurred. Please refer the errorInformation section for details.")


def read_message(filter_parameters: dict) -> Union[dict, list]:
    database_name: str = config.DATABASE_URL
    sql_query: str
    result_json: Union[dict, list]
    keys_list: list = []
    message_element: dict = {}
    try:
        for key, value in filter_parameters.items():
            keys_list.append(key)

        if filter_parameters in [None, '']:
            result_json = []
            sql_query = Query.MESSAGE_READ_ALL
            message_data_extract = db.dql_fetch_all_rows(database=database_name, sql_script=sql_query, return_list=False)
            for message_item in message_data_extract:
                message_element = {
                    "messageIdentifier": message_item[0],
                    "name": message_item[1],
                    "emailAddress": message_item[2],
                    "messageSubject": message_item[3],
                    "messageBody": message_item[4],
                    "messageReceivedDatetime": message_item[5],
                    "isMessageRead": True if message_item[6] == 1 else False
                }
                result_json.append(message_element)
        else:
            result_json = []
            if len(filter_parameters.items()) > 1:
                sql_query = db.query_builder_from_payload(base_query=Query.MESSAGE_READ_ALL, json_payload=filter_parameters, data_mapping=Map.READ_PAYLOAD_MESSAGES_MAPPING)
                message_data_extract = db.dql_fetch_all_rows(database=database_name, sql_script=sql_query, return_list=False)
                for message_item in message_data_extract:
                    message_element = {
                        "messageIdentifier": message_item[0],
                        "name": message_item[1],
                        "emailAddress": message_item[2],
                        "messageSubject": message_item[3],
                        "messageBody": message_item[4],
                        "messageReceivedDatetime": message_item[5],
                        "isMessageRead": True if message_item[6] == 1 else False
                    }
                    result_json.append(message_element)
            elif len(filter_parameters.items()) == 1:
                for key, item in filter_parameters.items():
                    sql_query = Map.READ_PAYLOAD_MESSAGES_MAPPING[key]
                    item = '1' if item else '0'
                    message_data_extract = db.dql_fetch_all_rows_for_one_input(database=database_name, sql_script=sql_query, return_list=False, data_input=item)
                    for message_item in message_data_extract:
                        message_element = {
                            "messageIdentifier": message_item[0],
                            "name": message_item[1],
                            "emailAddress": message_item[2],
                            "messageSubject": message_item[3],
                            "messageBody": message_item[4],
                            "messageReceivedDatetime": message_item[5],
                            "isMessageRead": True if message_item[6] == 1 else False
                        }
                        result_json.append(message_element)
            else:
                sql_query = Query.MESSAGE_READ_ALL
                message_data_extract = db.dql_fetch_all_rows(database=database_name, sql_script=sql_query, return_list=False)
                for message_item in message_data_extract:
                    message_element = {
                        "messageIdentifier": message_item[0],
                        "name": message_item[1],
                        "emailAddress": message_item[2],
                        "messageSubject": message_item[3],
                        "messageBody": message_item[4],
                        "messageReceivedDatetime": message_item[5],
                        "isMessageRead": True if message_item[6] == 1 else False
                    }
                    result_json.append(message_element)
        return result_json
    except Exception as error:
        return build.response_template(success=False, display_error=True, error=error, status_code=400, message="An error has occurred. Please refer the errorInformation section for details.")


def update_message_status(message_id):
    database_name: str = config.DATABASE_URL
    if message_exists(message_id):
        search_value = ''
        if type(message_id) is list:
            for i in message_id:
                search_value += f'{i},'
            search_value = search_value[:-1]
            data_input = {'?searchValue': search_value}
            db.dml_dql_execute_parameterized_script(database=database_name, sql_script=Query.MESSAGE_UPDATE_READ_STATUS, data_input_list=data_input)
            return build.response_template(success=True, display_error=False, status_code=200, message="Operation completed successfully.")
        elif type(message_id) in [str, int]:
            data_input = {'?searchValue': message_id}
            db.dml_dql_execute_parameterized_script(database=database_name, sql_script=Query.MESSAGE_UPDATE_READ_STATUS, data_input_list=data_input)
            return build.response_template(success=True, display_error=False, status_code=200, message="Operation completed successfully.")
        else:
            return build.response_template(success=False, display_error=True, status_code=400, message="An error has occurred.", error=err.InvalidRequest('Invalid payload. Please retry.'))
    else:
        return build.response_template(success=False, display_error=True, status_code=400, message="An error has occurred.", error=err.NoContent('The message you are trying to read has either been read already or it does not exist.'))


def _perform_update(payload: dict, database_name: str):
    id_name = payload['identifierName']
    id_value = payload['identifierValue']
    data_to_update = payload['updateKey']
    provided_old_value = payload['oldValue']
    new_value = payload['newValue']
    current_value = db.dql_fetch_one_row_for_one_input(database=database_name, sql_script=Map.UPDATE_PAYLOAD_MAPPING[id_name]['getCurrentValueQuery'], data_input=id_value)

    if current_value != provided_old_value:
        raise err.OldValueMismatch(message=f'Update could not be performed as the old value provided does not match with the value in the database. Please provide the accurate value to perform the update.')
    else:
        query_parameter_update_values: dict = {
            "?colName": Map.UPDATE_PAYLOAD_MAPPING[data_to_update]['dbColumnName'],
            "?data": new_value,
            "?searchValue": id_value,
        }
        db.dml_dql_execute_parameterized_script(database=database_name, sql_script=Map.UPDATE_PAYLOAD_MAPPING[id_name]['updateDataQuery'], data_input_list=query_parameter_update_values)


def _perform_insert_project(payload: dict, database_name: str):

    project_name = payload['projectName']
    project_summary = payload['projectSummary']
    project_image_path = payload['displayImageLocation']
    project_tech_stack_list = payload['technologyStackList']

    try:
        project_exists = db.dql_fetch_one_row_for_one_input(database=database_name, data_input=project_name, sql_script=Query.PROJECT_ID_BY_NAME)

        build_data_to_insert: str = f"'{project_name}', '{project_summary}', '{project_image_path}'" if project_image_path is not None else f"'{project_name}', '{project_summary}', NULL"

        if project_exists is None:
            query_parameter_project_insert_values: dict = {
                "?colList": f"{Map.INSERT_PAYLOAD_PROJECTS_MAPPING['projectName']}, "
                            f"{Map.INSERT_PAYLOAD_PROJECTS_MAPPING['projectSummary']}, "
                            f"{Map.INSERT_PAYLOAD_PROJECTS_MAPPING['displayImageLocation']}",
                "?data": build_data_to_insert
            }
            db.dml_dql_execute_parameterized_script(database=database_name, sql_script=Query.PROJECT_INSERT, data_input_list=query_parameter_project_insert_values)
            project_id = db.dql_fetch_one_row_for_one_input(database=database_name, data_input=project_name, sql_script=Query.PROJECT_ID_BY_NAME)
            for tech_item in project_tech_stack_list:
                query_parameter_tech_insert_values = {
                    "?colList": f"{Map.INSERT_PAYLOAD_PROJECTS_MAPPING['projectIdentifier']}, {Map.INSERT_PAYLOAD_PROJECTS_MAPPING['technologyStackList']}",
                    "?data": f"{project_id}, '{tech_item}'"
                }
                db.dml_dql_execute_parameterized_script(database=database_name, sql_script=Query.PROJECT_TECH_STACK_INSERT, data_input_list=query_parameter_tech_insert_values)
        else:
            raise err.DataExists(message=f"Project that you are trying to insert already exists in the database. [ProjectId = {project_exists}] Please check.")
    except Exception as error:
        raise error


def _perform_insert_message(payload: dict, database_name: str):

    message_name = payload['name']
    message_email = payload['emailAddress']
    message_subject = payload['messageSubject']
    message_body = payload['messageBody']
    message_received_date = datetime.now()

    try:
        build_data_to_insert: str = f"'{message_name}', '{message_email}', '{message_subject}', '{message_body}', '{message_received_date}'"
        query_parameter_project_insert_values: dict = {
            "?colList": f"{Map.INSERT_PAYLOAD_MESSAGES_MAPPING['name']}, "
                        f"{Map.INSERT_PAYLOAD_MESSAGES_MAPPING['emailAddress']}, "
                        f"{Map.INSERT_PAYLOAD_MESSAGES_MAPPING['messageSubject']},"
                        f"{Map.INSERT_PAYLOAD_MESSAGES_MAPPING['messageBody']},"
                        f"{Map.INSERT_PAYLOAD_MESSAGES_MAPPING['messageReceivedDatetime']}",
            "?data": build_data_to_insert
        }
        db.dml_dql_execute_parameterized_script(database=database_name, sql_script=Query.MESSAGE_ADD, data_input_list=query_parameter_project_insert_values)
    except Exception as error:
        raise error


def project_exists(project_id: Union[str, int]):
    data_extract = db.dql_fetch_one_row_for_one_input(database=config.DATABASE_URL, sql_script=Query.PROJECT_DETAILS_BY_ID, data_input=project_id)
    if data_extract is None:
        return False
    else:
        return True


def message_exists(message_id: Union[str, int, list]):
    search_value: str = ''
    if type(message_id) is list:
        for i in message_id:
            search_value += f'{i},'
        search_value = search_value[:-1]
    else:
        search_value = message_id
    data_extract = db.dql_fetch_one_row_for_one_input(database=config.DATABASE_URL, sql_script=Query.MESSAGE_READ_UNREAD_BY_ID, data_input=search_value)
    
    if data_extract is None:
        return False
    else:
        return True


def process_chat(data: Union[dict, list], chat_log):
    message = data['message']
    timestamp = data['timestamp']
    if message:
        chat_log.append({'sender': 'user', 'text': message, 'timestamp': timestamp})
        response_timestamp = datetime.now().strftime("%Y-%m-%d %I:%M %p")
        chat_log.append({'sender': 'admin', 'text': "Thanks for your message!", 'timestamp': response_timestamp})
    print(chat_log)
    return None
