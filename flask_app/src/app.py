import os
import pprint
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".."))
)

from flask import Flask, jsonify, make_response
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from src.config import settings
from src.models import producer

from flask_app.docs.api_spec import get_apispec
from flask_app.docs.swagger import SWAGGER_URL, swagger_ui_blueprint
from http import HTTPStatus

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["10 per second"],
)
jwt = JWTManager()


def create_app(config_object=settings):
    app = Flask(__name__)
    app.config.update(config_object)

    jwt.init_app(app=app)
    limiter.init_app(app=app)

    from src.routes import api_bp

    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    @app.route("/")
    @limiter.limit("1 per second")
    def home():
        return "Hello, Flask!"

    @app.route("/health", methods=["GET"])
    def healthcheck():
        health_status = {
            "status": "ok",
            "message": "Service is healthy",
        }
        return jsonify(health_status), HTTPStatus.OK

    @app.route("/test_kafka", methods=["GET"])
    def test_kafka():
        try:
            test_message = {
                "user": "test_user",
                "action": "test",
                "data": {"message": "This is a test message"},
            }
            producer.send(
                topic="test_topic",
                key={"user": "test_user"},
                value=test_message,
            )
            producer.flush()
            return jsonify({"msg": "Test message sent to Kafka"}), HTTPStatus.OK
        except Exception as e:
            return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

    @app.route("/swagger")
    def create_swagger_spec():
        return jsonify(get_apispec(app).to_dict())

    @app.errorhandler(HTTPStatus.NOT_FOUND)
    def not_found(error):
        return make_response(jsonify({"error": "Not found"}), HTTPStatus.NOT_FOUND)

    @app.errorhandler(HTTPStatus.TOO_MANY_REQUESTS)
    def ratelimit_handler(e):
        return make_response(jsonify(error=f"ratelimit exceeded {e.description}"), HTTPStatus.TOO_MANY_REQUESTS)

    return app
