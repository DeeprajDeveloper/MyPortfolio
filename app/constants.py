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


class QueryReadData:
    PROJECT_NAMES = r"SELECT projectName from projects where activeProject = 1"
    PROJECT_SUMMARY = r"SELECT projectName, projectDescription, imagePath from projects where activeProject = 1"
    PROJECT_EXTENSIVE_DETAIL = r""
