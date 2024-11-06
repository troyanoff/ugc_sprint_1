import logging
from functools import wraps

from flask import request
from src.config import settings


def log_request_in_dev(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "localhost" in settings.KAFKA_BOOTSTRAP_SERVERS:
            logging.info(f"Request to {request.path} with data {request.json}")
        return f(*args, **kwargs)

    return decorated_function
