import functools
from datetime import datetime

from flask import g, request

from corefw.appfw.services.apikeys_services import ApiKeysService
from corefw.constants.constants import ASSOCIATED_GROUPS, LAST_USED, NAME, X_API_KEY
from corefw.constants.messages import EMPTY_API_KEY, FORBIDDEN_ACCESS, INVALID_API_KEY
from corefw.exceptionsfw.exceptions import GatewayException
from corefw.loggerfw import logger

LOGGER = logger.get_logger(__name__)


def auth(logger, route_name):
    """
    Use @auth to athorise and set globals
    :return:
    """

    def authorize(func):
        """
        Decorator to authorize and set globals
        :param func:
        :return:
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = datetime.utcnow()
            try:

                AuthorizationUtils().is_empty_apikey()
                AuthorizationUtils().validate(route_name=route_name)
                logger.info("Calling function from authorize")
                response, status_code, code = func(*args, **kwargs)

                return response, status_code, code
            except GatewayException as gateway_exception:
                logger.exception(gateway_exception)
                raise
            except Exception as exception:
                logger.exception(exception)
                raise
            finally:
                time_taken = datetime.utcnow() - start_time
                logger.info(
                    "Exit function : %s Time taken : %s", func.__name__, time_taken
                )

        return wrapper

    return authorize


class AuthorizationUtils:
    """
    Authorization Utils
    """

    def is_empty_apikey(self):
        """
        Check empty apikey
        :return:
        """
        api_key = request.headers.get(X_API_KEY)
        if not api_key:
            raise GatewayException(message=EMPTY_API_KEY, status=400)

    def validate(self, route_name):
        """
        Validate api key and group
        """
        api_key = request.headers.get(X_API_KEY)
        get_api_details = ApiKeysService().get_apikey_details(api_key=api_key)

        if not get_api_details:
            raise GatewayException(message=INVALID_API_KEY, status=404)

        g.identifier = get_api_details.get(NAME)
        apikey_apps = ApiKeysService(collection_name="groups").get_associated_apps(
            get_api_details.get(ASSOCIATED_GROUPS)
        )
        LOGGER.info("apps list %s:", str(apikey_apps))
        api_key_update = {LAST_USED: True}
        if "*" in apikey_apps:
            ApiKeysService().update_api_key(api_key=api_key, **api_key_update)
            return
        if route_name not in apikey_apps:
            raise GatewayException(message=FORBIDDEN_ACCESS, status=403)
        ApiKeysService().update_api_key(api_key=api_key, **api_key_update)
