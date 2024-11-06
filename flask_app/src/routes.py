from typing import Literal

from flask import Blueprint, jsonify, request
from flask.wrappers import Response
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus
from src.app import limiter
from src.models import producer
from src.utils import log_request_in_dev

api_bp = Blueprint("api", __name__)


@api_bp.route("/<action>", methods=["POST"])
@jwt_required()
@log_request_in_dev
@limiter.limit("10 per second")
def log_action(action) -> tuple[Response, Literal[400] | Literal[200]]:
    
    if action not in ["click", "view", "quality_change", "video_progress", "query"]:
        return jsonify({"msg": "Invalid action"}), HTTPStatus.BAD_REQUEST

    user = get_jwt_identity()
    data = request.json

    topic = f"{action}_events"
    producer.send(
        topic=topic,
        value=data,
    )

    return jsonify({"msg": f"{action.capitalize()} logged"}), HTTPStatus.OK
