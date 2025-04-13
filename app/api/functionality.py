import config
from typing import Union, List
from app.constants import (QueryString as Query, ResponseKeysList as Keys, ValidIdentifiers as ValidIds, Mapping as Map)
from utils import (custom_error as err, db_util as db, build_json_response as build)


def get_project_summary(filter_parameters: str):
    database_name: str = config.DATABASE_URL

    project_summary: list
    project_ids: list
    project_techstack: list = []
    result_json: List[dict] = []
    project_element: dict = {}

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
    old_value: str
    new_value: str
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
                        _perform_insert(payload=insert_item, database_name=database_name)
                    else:
                        raise err.InvalidPayload(message=f'Payload is missing certain parameters. Payload must contain {ValidIds.UPDATE_PAYLOAD_KEYS}. Please revalidate the payload and retry the operation.')
            else:
                for key, value in insert_payload.items():
                    keys_list.append(key)
                if keys_list == ValidIds.INSERT_PAYLOAD_PROJECT_KEYS:
                    _perform_insert(payload=insert_payload[0], database_name=database_name)
                else:
                    raise err.InvalidPayload(message=f'Payload is missing certain parameters. Payload must contain {ValidIds.UPDATE_PAYLOAD_KEYS}. Please revalidate the payload and retry the operation.')

        elif json_input['action'] in ValidIds.OPERATIONS and json_input['action'] != 'I':
            raise err.InvalidAction(message=f'Action {json_input["action"]} not allowed for this api endpoint.')
        else:
            raise err.InvalidOperation(message=f"Operation {json_input['action']} provided is invalid")

        return build.response_template(success=True, display_error=False, status_code=200, message="Operation completed successfully.")
    except Exception as error:
        return build.response_template(success=False, display_error=True, error=error, status_code=400, message="An error has occurred. Please refer the errorInformation section for details.")


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


def _perform_insert(payload: dict, database_name: str):

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


def project_exists(project_id: Union[str, int]):
    data_extract = db.dql_fetch_one_row_for_one_input(database=config.DATABASE_URL, sql_script=Query.PROJECT_DETAILS_BY_ID, data_input=project_id)
    if data_extract is None:
        return False
    else:
        return True
