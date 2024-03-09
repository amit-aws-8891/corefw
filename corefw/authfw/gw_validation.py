import functools
import re
from http import HTTPStatus

from flask import request
from src.specs.constants.constants import DATA, EMAIL, EMAIL_ID, IP_ADDRESS, USER_EMAIL
from src.specs.constants.messages import (
    INVALID_DATA_OBJECT,
    INVALID_EMAIL_ADDRESS,
    INVALID_IP_ADDRESS,
)
from src.specs.exceptions.exceptions import GatewayException

EMAIL_REGEX = re.compile(r"\S+@\S+\.\S+")
URI_REGEX = re.compile(r"(http|https|ftp)://\S+\.\S+")
IP_REGEX = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")


def gw_validator(func):
    """
    Field validation
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        request_body = request.get_json()
        # validate args here
        if EMAIL in request_body and not bool(
            EMAIL_REGEX.match(request_body.get(EMAIL))
        ):
            raise GatewayException(
                message=INVALID_EMAIL_ADDRESS, status=HTTPStatus.BAD_REQUEST
            )
        if USER_EMAIL in request_body and not bool(
            EMAIL_REGEX.match(request_body.get(USER_EMAIL))
        ):
            raise GatewayException(
                message=INVALID_EMAIL_ADDRESS, status=HTTPStatus.BAD_REQUEST
            )
        if EMAIL_ID in request_body.get(DATA) and not bool(
            EMAIL_REGEX.match(request_body.get(DATA).get(EMAIL_ID))
        ):
            raise GatewayException(
                message=INVALID_EMAIL_ADDRESS, status=HTTPStatus.BAD_REQUEST
            )
        if IP_ADDRESS in request_body and not bool(
            IP_REGEX.match(request_body.get(IP_ADDRESS))
        ):
            raise GatewayException(
                message=INVALID_IP_ADDRESS, status=HTTPStatus.BAD_REQUEST
            )
        if DATA in request_body and len(request_body.get(DATA)) == 0:
            raise GatewayException(
                message=INVALID_DATA_OBJECT, status=HTTPStatus.BAD_REQUEST
            )
        return func(*args, **kwargs)

    return wrapper
