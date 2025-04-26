from flask import Flask, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
import config
from app.api.routes import bp_api
from app.auth.routes import bp_auth, jwt
from app.gui.views import bp_gui

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
app.config['SECRET_KEY'] = config.APP_SECRET_KEY
jwt.init_app(app)
app.json.sort_keys = False
app.register_blueprint(bp_gui)
app.register_blueprint(bp_api)
app.register_blueprint(bp_auth)

swagger_document = get_swaggerui_blueprint(config.SWAGGER_ENDPOINT, config.SWAGGER_API_URL, config=config.SWAGGER_CONFIG)
app.register_blueprint(swagger_document, url_prefix=config.SWAGGER_ENDPOINT)


@app.route("/swagger.json")
def send_swagger():
    return send_from_directory("mainApp/doc/static", "swagger.json")


if __name__ == "__main__":
    print(f"{config.APP_NAME} started running on {config.HOST}:{config.PORT} - Debug mode is {'on' if config.DEBUG else 'off'}")
    app.run(debug=config.DEBUG, port=config.PORT, host=config.HOST)
