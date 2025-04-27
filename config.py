import os

basedir = os.path.abspath(os.path.dirname(__file__))
APP_NAME = os.getenv("APP_NAME", "MyPortfolio")
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1")
DATABASE_URL = os.getenv("DATABASE_URL", fr"{basedir}/database/portfolio.db")
PORT = 701
HOST = '127.0.0.1'
APP_SECRET_KEY = 'L4@G5W6E'

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
