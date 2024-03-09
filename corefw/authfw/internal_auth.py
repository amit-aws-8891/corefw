import base64
from datetime import datetime

from flask import current_app, request
from flask_restx import abort

from corefw.constants.constants import X_API_KEY
from corefw.loggerfw import logger

LOGGER = logger.get_logger(__name__)


def internal_auth(func):
    """
    Decorator to authenticate internal apis
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        start_time = datetime.utcnow().timestamp()
        try:
            InternalAuthUtils().validate()
            # logger.info("Calling function from authorize")

            return func(*args, **kwargs)
        except Exception as exception:
            LOGGER.exception(exception)
            raise
        finally:
            time_taken = datetime.utcnow().timestamp() - start_time
            LOGGER.info(
                "Exit function : %s, Time taken(s) : %d", func.__name__, time_taken
            )

    return wrapper


class InternalAuthUtils:
    """
    Authorization Utils
    """

    def validate(self):
        """
        Validate api key
        """
        api_key = request.headers.get(X_API_KEY)
        if not api_key:
            abort(400, "Please provide api key")
        token = base64.b64decode(current_app.config["service_token"]).decode("utf-8")
        internal_token = request.headers.get(X_API_KEY)
        if token != internal_token:
            abort(401, "Invalid api key")
