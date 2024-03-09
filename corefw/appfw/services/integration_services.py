import uuid

from flask import current_app
from flask_restx import abort

from corefw import get_settings
from corefw.constants.constants import (
    CREDENTIALS,
    INTEGRATION_ID,
    NAME,
    PROVIDER_CODE,
    SALT_KEY,
    VALUE,
)
from corefw.constants.messages import PROVIDER_NOT_FOUND
from corefw.exceptionsfw.exceptions import DataBaseException
from corefw.loggerfw.logger import get_logger
from corefw.models.v1.schema import IntegrationSchema, UpdateIntegrationSchema
from corefw.mongofw.data_access import DataAccessObject

LOGGER = get_logger(__name__)


class IntegrationService:
    def __init__(self, collection_name="integrations"):
        self.collection_name = collection_name

    def get_integration(self, provider_code):
        """
        Get Provider code
        """
        credentials = []
        filter_dict = {PROVIDER_CODE: provider_code}
        get_resource = DataAccessObject(
            collection_name=get_settings(current_app, "INTEGRATION_COLLECTION")
        ).get_resource(filter_dict=filter_dict, project_fields={"_id": 0, SALT_KEY: 0})
        if not get_resource:
            abort(404, PROVIDER_NOT_FOUND[1])
        for row in get_resource.get(CREDENTIALS):
            credentials.append({NAME: row.get(NAME), VALUE: "***********"})
        get_resource[CREDENTIALS] = credentials
        return get_resource, 200

    def create_integration(self, **data):
        """
        Create integration
        """
        try:
            integration_id = str(uuid.uuid4())
            integration_model = IntegrationSchema(**data)
            integration_model[INTEGRATION_ID] = integration_id
            credential_indexes = [
                {
                    "indexname": "integration_id_index",
                    "field_name": INTEGRATION_ID,
                    "is_unique": True,
                },
                {
                    "indexname": "integration_provider_index",
                    "field_name": PROVIDER_CODE,
                    "is_unique": True,
                },
            ]
            DataAccessObject(
                collection_name=get_settings(current_app, "INTEGRATION_COLLECTION")
            ).create_indexes(indexes=credential_indexes)
            DataAccessObject(
                collection_name=get_settings(current_app, "INTEGRATION_COLLECTION")
            ).create(data=integration_model)

            return integration_id, 201
        except DataBaseException as exception:
            LOGGER.exception(exception)
            abort(500, str(exception))
            raise

    def update_integration(self, provider_code, **data):
        """
        Create integration
        """
        try:
            filter_dict = {PROVIDER_CODE: provider_code}
            get_resource = DataAccessObject(
                collection_name=get_settings(current_app, "INTEGRATION_COLLECTION")
            ).get_resource(filter_dict=filter_dict)
            if not get_resource:
                abort(404, PROVIDER_NOT_FOUND[1])
            integration_model = UpdateIntegrationSchema(**data)
            DataAccessObject(
                collection_name=get_settings(current_app, "INTEGRATION_COLLECTION")
            ).update(data=integration_model, filter_dict=filter_dict)

            return "success", 200
        except DataBaseException as exception:
            LOGGER.exception(exception)
            abort(500, str(exception))
            raise

    def delete_integration(self, provider_code):
        try:
            filter_dict = {PROVIDER_CODE: provider_code}
            get_resource = DataAccessObject(
                collection_name=get_settings(current_app, "INTEGRATION_COLLECTION")
            ).get_resource(filter_dict=filter_dict)
            if not get_resource:
                abort(404, PROVIDER_NOT_FOUND[1])

            DataAccessObject(
                collection_name=get_settings(current_app, "INTEGRATION_COLLECTION")
            ).delete(filter_dict=filter_dict)

            return "success", 200
        except DataBaseException as exception:
            LOGGER.exception(exception)
            abort(500, str(exception))

    def get_sandbox_integration(self, provider_code):
        """
        Get Provider code
        """
        credentials = []
        filter_dict = {PROVIDER_CODE: provider_code}
        get_resource = DataAccessObject(
            collection_name=get_settings(current_app, "SANDBOX_INTEGRATION_COLLECTION")
        ).get_resource(filter_dict=filter_dict, project_fields={"_id": 0, SALT_KEY: 0})
        if not get_resource:
            abort(404, PROVIDER_NOT_FOUND[1])
        for row in get_resource.get(CREDENTIALS):
            credentials.append({NAME: row.get(NAME), VALUE: "***********"})
        get_resource[CREDENTIALS] = credentials
        return get_resource, 200

    def create_sandbox_integration(self, **data):
        """
        Create integration
        """
        try:
            integration_id = str(uuid.uuid4())
            integration_model = IntegrationSchema(**data)
            integration_model[INTEGRATION_ID] = integration_id
            credential_indexes = [
                {
                    "indexname": "integration_id_index",
                    "field_name": INTEGRATION_ID,
                    "is_unique": True,
                },
                {
                    "indexname": "integration_provider_index",
                    "field_name": PROVIDER_CODE,
                    "is_unique": False,
                },
            ]
            DataAccessObject(
                collection_name=get_settings(
                    current_app, "SANDBOX_INTEGRATION_COLLECTION"
                )
            ).create_indexes(indexes=credential_indexes)
            DataAccessObject(
                collection_name=get_settings(
                    current_app, "SANDBOX_INTEGRATION_COLLECTION"
                )
            ).create(data=integration_model)

            return integration_id, 201
        except DataBaseException as exception:
            LOGGER.exception(exception)
            abort(500, str(exception))
            raise

    def update_sandbox_integration(self, provider_code, **data):
        """
        Create integration
        """
        try:
            filter_dict = {PROVIDER_CODE: provider_code}
            get_resource = DataAccessObject(
                collection_name=get_settings(
                    current_app, "SANDBOX_INTEGRATION_COLLECTION"
                )
            ).get_resource(filter_dict=filter_dict)
            if not get_resource:
                abort(404, PROVIDER_NOT_FOUND[1])
            integration_model = UpdateIntegrationSchema(**data)
            DataAccessObject(
                collection_name=get_settings(
                    current_app, "SANDBOX_INTEGRATION_COLLECTION"
                )
            ).update(data=integration_model, filter_dict=filter_dict)

            return "success", 200
        except DataBaseException as exception:
            LOGGER.exception(exception)
            abort(500, str(exception))

    def delete_sandbox_integration(self, provider_code):
        try:
            filter_dict = {PROVIDER_CODE: provider_code}
            get_resource = DataAccessObject(
                collection_name=get_settings(current_app, "INTEGRATION_COLLECTION")
            ).get_resource(filter_dict=filter_dict)
            if not get_resource:
                abort(404, PROVIDER_NOT_FOUND[1])

            DataAccessObject(
                collection_name=get_settings(
                    current_app, "SANDBOX_INTEGRATION_COLLECTION"
                )
            ).delete(filter_dict=filter_dict)

            return "success", 200
        except DataBaseException as exception:
            LOGGER.exception(exception)
            abort(500, str(exception))
