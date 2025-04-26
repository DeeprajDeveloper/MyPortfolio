class Information:
    VERSION: str = 'v.1.0.0.20250210'
    AUTHOR: str = 'Adhikary, Deepraj'
    CREATE_DATE: str = 'Mar 18, 2025'
    RELEASE_DATE: str = 'Mar 18, 2025'
    JOB_START_YEAR: int = 2018
    JOB_START_MONTH_ID: int = 6


class Logging:
    LOG_DIRECTORY: str = r".\logs"
    LOG_FILENAME: str = r'app_log.log'


class QueryString:

    # Project related Information
    PROJECT_NAMES: str = r"SELECT projectName FROM projects"
    PROJECT_ALL_IDS: str = r"SELECT projectId FROM projects"
    PROJECT_ALL_SUMMARY: str = r"SELECT projectId, projectName, projectDescription, imagePath FROM projects"
    PROJECT_SUMMARY_BY_ID: str = r"SELECT projectName, projectDescription, imagePath, activeProject FROM projects WHERE projectId = ?searchValue"
    PROJECT_TECH_STACK: str = r"SELECT techStackName FROM projectTechStack where projectId = ?searchValue"
    PROJECT_TECH_STACK_INSERT: str = r"INSERT INTO projectTechStack (?colList) VALUES (?data)"
    PROJECT_INSERT: str = r"INSERT INTO projects (?colList) VALUES (?data)"
    PROJECT_ID_BY_NAME: str = r"SELECT projectId from projects where projectName like '%?searchValue%'"
    PROJECT_DETAILS_BY_ID = r"SELECT overview, problemStatement, solutionApproach, hasPreview, hasGitRepo, linkGitRepo, linkPreview from projectDetails where projectId = ?searchValue"

    # General Information
    GENERAL_INFO_LIST: str = r"SELECT keyName, dataValue FROM generalInformation ORDER BY rowId ASC"
    GENERAL_DATAVALUE_BY_KEY: str = r"SELECT dataValue FROM generalInformation WHERE keyName = '?searchValue'"
    GENERAL_DATAVALUE_BY_ID: str = r"SELECT dataValue FROM generalInformation WHERE rowId = ?searchValue"

    # Expertise  Information
    EXPERTISE_LIST: str = r"SELECT expertiseId, expertiseName, iconImagePath FROM expertiseInformation ORDER BY expertiseId ASC"
    EXPERTISE_GET_ALL_BY_ID: str = r"SELECT expertiseName, iconImagePath FROM expertiseInformation WHERE expertiseId = ?searchValue"
    EXPERTISE_UPDATE_BY_ID: str = r"UPDATE expertiseInformation SET ?colName = '?data' WHERE expertiseId = ?searchValue"

    # Experience  Information
    EXPERIENCE_LIST: str = r"SELECT experienceId, experienceName, experienceYears FROM industryExperienceInformation ORDER BY experienceId ASC"
    EXPERIENCE_GET_ALL_BY_ID: str = r"SELECT experienceName, experienceYears FROM industryExperienceInformation WHERE experienceId = ?searchValue"
    EXPERIENCE_GET_ID_BY_NAME: str = r"SELECT experienceId FROM industryExperienceInformation WHERE experienceName = ?searchValue"
    EXPERIENCE_UPDATE_BY_ID: str = r"UPDATE industryExperienceInformation SET ?colName = '?data' WHERE experienceId = ?searchValue"

    # Messages
    MESSAGE_ADD: str = r"INSERT INTO inquiryMessages (?colList) VALUES (?data)"
    MESSAGE_UPDATE: str = r"UPDATE inquiryMessages SET ?colName = ?data WHERE messageId in (?searchValue)"
    MESSAGE_READ_ALL: str = r"SELECT * FROM inquiryMessages"
    MESSAGE_READ_BY_ID: str = r"SELECT * FROM inquiryMessages WHERE messageId = ?searchValue"
    MESSAGE_READ_BY_ISREAD: str = r"SELECT * FROM inquiryMessages WHERE isRead = ?searchValue"
    MESSAGE_READ_BY_NAME: str = r"SELECT * FROM inquiryMessages WHERE requestorName = '?searchValue'"
    MESSAGE_READ_BY_EMAIL: str = r"SELECT * FROM inquiryMessages WHERE requestorEmailAddress = '?searchValue'"
    MESSAGE_READ_UNREAD_BY_ID: str = r"SELECT * FROM inquiryMessages WHERE isRead = 0 and messageId in (?searchValue)"
    MESSAGE_UPDATE_READ_STATUS: str = r"UPDATE inquiryMessages SET isRead = 1 WHERE messageId in (?searchValue)"



class ResponseKeysList:
    EXPERTISE_KEYS: list = ['expertiseId', 'expertiseName', 'iconImagePath']
    EXPERIENCE_KEYS: list = ['experienceId', 'experienceName', 'yearsExperienceDisplayText']


class ValidIdentifiers:
    DATA_IDENTIFIERS: list = ['experienceId', 'expertiseId']
    UPDATE_PAYLOAD_KEYS: list = ['identifierName', 'identifierValue', 'updateKey', 'oldValue', 'newValue']
    INSERT_PAYLOAD_PROJECT_KEYS: list = ['projectName', 'projectSummary', 'technologyStackList', 'displayImageLocation']
    INSERT_PAYLOAD_MESSAGE_KEYS: list = ['name', 'emailAddress', 'messageSubject', 'messageBody']
    READ_PAYLOAD_MESSAGE_KEYS: list = ['name', 'emailAddress', 'messageSubject', 'messageBody', 'messageReceivedDatetime', 'isMessageRead']
    OPERATIONS: list = ['I', 'U', 'D']


class Mapping:
    UPDATE_PAYLOAD_MAPPING: dict = {
        "experienceId": {
            "dbColumnName": "experienceId",
            "updateDataQuery": QueryString.EXPERIENCE_UPDATE_BY_ID,
            "getCurrentValueQuery": QueryString.EXPERIENCE_GET_ALL_BY_ID
        },
        "expertiseId": {
            "dbColumnName": "expertiseId",
            "updateDataQuery": QueryString.EXPERTISE_UPDATE_BY_ID,
            "getCurrentValueQuery": QueryString.EXPERTISE_GET_ALL_BY_ID
        },
        "expertiseName": {
            "dbColumnName": "expertiseName"
        },
        "experienceName": {
            "dbColumnName": "experienceName"
        }
    }
    INSERT_PAYLOAD_PROJECTS_MAPPING: dict = {
        "projectIdentifier": "projectId",
        "projectName": "projectName",
        "projectSummary": "projectDescription",
        "displayImageLocation": "imagePath",
        "technologyStackList": 'techStackName'
    }
    INSERT_PAYLOAD_MESSAGES_MAPPING: dict = {
        "name": "requestorName",
        "emailAddress": "requestorEmailAddress",
        "messageSubject": "subjectLine",
        "messageBody": "messageDescription",
        "messageReceivedDatetime": "sentDatetime"
    }
    READ_PAYLOAD_MESSAGES_MAPPING: dict = {
        "name": QueryString.MESSAGE_READ_BY_NAME,
        "emailAddress": QueryString.MESSAGE_READ_BY_EMAIL,
        "messageIdentifier": QueryString.MESSAGE_READ_BY_ID,
        "isMessageRead": QueryString.MESSAGE_READ_BY_ISREAD
    }


class AppDataConstants:
    RANDOM_PROJECT_GEN_COUNT = 1
