import os

basedir = os.path.abspath(os.path.dirname(__file__))
APP_NAME = 'MyPortfolio'
DEBUG = True
DATABASE_URL = fr"{basedir}/database/portfolio.db"
# MY_INFO_JSON = fr"{basedir}/database/myInformation.json"
PORT = 701
HOST = '127.0.0.1'

SWAGGER_ENDPOINT = "/api/docs"
SWAGGER_API_URL = f"/swagger.json"
SWAGGER_CONFIG = {
    "app_name": "Portfolio | API Doc",
    "layout": "BaseLayout",  # Options: "BaseLayout", "StandaloneLayout", "Topbar"
    "deepLinking": True,
    "displayOperationId": True,
    "defaultModelsExpandDepth": -1,
    "defaultModelRendering": "model",
}
