import base64
import functools
import http

from cryptography.fernet import Fernet
from flask import current_app, g, request

from corefw import get_settings
from corefw.constants.constants import (
    CONFIG_DATA,
    CREDENTIALS,
    INTEGRATION_ID,
    NAME,
    PROVIDER_CODE,
    SALT_KEY,
    SANDBOX,
    VALUE,
)
from corefw.constants.messages import INTEGRATION_NOT_FOUND
from corefw.exceptionsfw.exceptions import GatewayException
from corefw.loggerfw import logger
from corefw.mongofw.data_access import DataAccessObject

LOGGER = logger.get_logger(__name__)


def integration(provider):
    """
    Integration decorator
    """

    def integration_func(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                collection_name = get_settings(current_app, "INTEGRATION_COLLECTION")
                if request.args.get(SANDBOX) == "true":
                    collection_name = get_settings(
                        current_app, "SANDBOX_INTEGRATION_COLLECTION"
                    )
                filter_dict = {PROVIDER_CODE: provider}
                integration_detail = DataAccessObject(
                    collection_name=collection_name
                ).get_resource(filter_dict)
                if not integration_detail:
                    raise GatewayException(
                        message=INTEGRATION_NOT_FOUND,
                        status=http.HTTPStatus.BAD_REQUEST,
                    )
                credentials = []
                salt_key = base64.b64decode(integration_detail.get(SALT_KEY))
                fernet = Fernet(salt_key)
                for row in integration_detail.get(CREDENTIALS):
                    credentials.append(
                        {
                            NAME: row.get(NAME),
                            VALUE: fernet.decrypt(row.get(VALUE)).decode(),
                        }
                    )
                g.credentials = credentials
                g.config_data = integration_detail.get(CONFIG_DATA, {})
                g.integration_id = integration_detail.get(INTEGRATION_ID)
                return func(*args, **kwargs)
            except Exception as exception:
                LOGGER.exception(exception)
                raise

        return wrapper

    return integration_func
