import itertools
import uuid
from http import HTTPStatus

from flask import current_app

from corefw import get_settings
from corefw.constants.constants import API_KEY, ASSOCIATED_APPS
from corefw.constants.messages import (
    DUPLICATE_APIKEY_NAME,
    DUPLICATE_GROUP_NAME,
    FAILED_TO_CREATE_API_KEY,
    FAILED_TO_CREATE_GROUP,
    FAILED_TO_GET_APIKEY_DETAILS,
    FAILED_TO_GET_ASSOCIATED_APPS,
    FAILED_TO_UPDATE_API_KEY,
)
from corefw.exceptionsfw.exceptions import DataBaseException, GatewayException
from corefw.loggerfw.logger import get_logger
from corefw.models.v1.schema import APIGroupSchema, ApiKeySchema, ApiKeyUpdateSchema
from corefw.mongofw.data_access import DataAccessObject

LOGGER = get_logger(__name__)


class ApiKeysService:
    """
    APIkey service
    """

    def __init__(self, collection_name=None):
        self.collection_name = collection_name

    def get(self, api_key_code):
        """

        :param api_key_code:
        :return:
        """
        ...

    def get_apikey_details(self, api_key):
        """
        Get API details
        """

        try:
            filter_dict = {"api_key": api_key}
            get_api_key = DataAccessObject(
                collection_name=get_settings(current_app, "APIKEY_COLLECTION")
            ).get_resource(filter_dict=filter_dict)
            return get_api_key
        except DataBaseException as db_ex:
            LOGGER.error(db_ex)
            raise GatewayException(
                message=FAILED_TO_GET_APIKEY_DETAILS, exception=db_ex
            )

    def get_associated_apps(self, group_list):
        """
        Get associated apps
        """

        try:
            filter_dict = {"name": {"$in": group_list}}
            apps = []
            groups = DataAccessObject(
                collection_name=get_settings(current_app, "GROUPS_COLLECTION")
            ).find_all_with_collation(filter_dict=filter_dict, sort_by="name")
            for row in groups:
                apps.append(row.get(ASSOCIATED_APPS))
            if apps:
                apps = list(set(itertools.chain.from_iterable(apps)))
            return apps
        except DataBaseException as db_ex:
            LOGGER.error(db_ex)
            raise GatewayException(
                message=FAILED_TO_GET_ASSOCIATED_APPS, exception=db_ex
            )

    def update_api_key(self, api_key, **data):
        """
        Update API key here
        """
        try:
            api_key_data = ApiKeyUpdateSchema(**data)
            filter_dict = {API_KEY: api_key}
            DataAccessObject().update(data=api_key_data, filter_dict=filter_dict)
            return "success", 200
        except DataBaseException as db_ex:
            LOGGER.error(db_ex)
            raise GatewayException(message=FAILED_TO_UPDATE_API_KEY, exception=db_ex)

    def create_api_key(self, **data):
        """
        Create API key
        """
        try:
            indexes = [
                {
                    "indexname": "apikey_name_index",
                    "field_name": "name",
                    "is_unique": True,
                },
                {
                    "indexname": "apikey_api_keys_index",
                    "field_name": "api_key",
                    "is_unique": True,
                },
            ]
            DataAccessObject().create_indexes(indexes=indexes)
            api_key = str(uuid.uuid4()) + str(uuid.uuid4())
            api_key = api_key.replace("-", "")
            data["api_key"] = api_key
            apikey_model = ApiKeySchema(**data)
            DataAccessObject().create(data=apikey_model)
            return api_key, 201
        except DataBaseException as exception:
            LOGGER.error(exception.error)
            if "duplicate key" in exception.error:
                raise GatewayException(message=DUPLICATE_APIKEY_NAME, status=409)
            # else:
            raise GatewayException(
                message=FAILED_TO_CREATE_API_KEY,
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

    def create_group(self, **data):
        """
        Create Group here
        """
        try:
            # create index
            indexes = [
                {
                    "indexname": "group_name_index",
                    "field_name": "name",
                    "is_unique": True,
                }
            ]
            DataAccessObject(
                collection_name=get_settings(current_app, "GROUPS_COLLECTION")
            ).create_indexes(indexes=indexes)
            api_group = APIGroupSchema(**data)
            DataAccessObject(
                collection_name=get_settings(current_app, "GROUPS_COLLECTION")
            ).create(data=api_group)
            return "success", 201
        except DataBaseException as exception:
            LOGGER.error(exception.error)
            if "duplicate key" in exception.error:
                raise GatewayException(
                    message=DUPLICATE_GROUP_NAME, exception=exception, status=409
                )
            raise GatewayException(
                message=FAILED_TO_CREATE_GROUP,
                exception=exception,
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

    def get_group_list(self):
        """
        Get Group list
        """
        try:
            filter_dict = {}
            groups = DataAccessObject(
                collection_name=get_settings(current_app, "GROUPS_COLLECTION")
            ).find_all_with_collation(filter_dict=filter_dict, sort_by="name")
            return groups, 200
        except DataBaseException as exception:
            LOGGER.error(exception)
            if "duplicate_key" in exception.error:
                raise GatewayException(message="Name already exist", status=409)
            raise GatewayException(
                message=str(exception), status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
