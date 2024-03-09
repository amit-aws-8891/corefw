from http import HTTPStatus

from src.specs.constants.constants import (
    DATABASE_ERROR,
    EXCEPTION,
    MESSAGE,
    RESPONSE_PARAMS,
    STATUS,
)
from src.specs.constants.messages import UNKNOWN_ERROR
from src.specs.models.response import Response


class GatewayException(Exception):
    """
     Exceptions raised in Service layer should be wrapped as ActionFacadeException.
    :param code: Refer message_codes
    :param exception: Original exception. ex will be logged.
    error_message.USER_DEFINED if exception is user created
    :param status: Http Status code.
    :param params: Translate params.
    """

    def __init__(
        self,
        message=UNKNOWN_ERROR,
        exception="user-defined",
        response_params=None,
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    ):
        super(GatewayException, self).__init__(message)
        super(GatewayException, self).__setattr__(MESSAGE, message)
        super(GatewayException, self).__setattr__(EXCEPTION, exception)
        super(GatewayException, self).__setattr__(STATUS, status)
        super(GatewayException, self).__setattr__(
            RESPONSE_PARAMS, response_params or []
        )

    def response(self) -> (Response, HTTPStatus):
        """
        Returns the standard response from the instance of ActionFacadeException
        :return: (Response, HTTPStatus)
        """
        status = getattr(self, STATUS, repr(self))
        message = getattr(self, MESSAGE, repr(self))
        response_params = getattr(self, RESPONSE_PARAMS, repr(self))
        return (
            dict(Response(message=message, response_params=response_params)),
            status,
        )


class DataBaseException(Exception):
    """Exceptions raised from database layer should be wrapped as DataBaseException"""

    def __init__(self, message=None, status=HTTPStatus.INTERNAL_SERVER_ERROR):
        self.error = message if message else DATABASE_ERROR
        self.status = status
        super(DataBaseException, self).__init__(self.error)
