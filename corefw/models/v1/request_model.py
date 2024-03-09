from flask_restx import fields
from src.specs.constants.constants import (
    API_KEY,
    ASSOCIATED_APPS,
    ASSOCIATED_GROUPS,
    CLIENT,
    CLIENT_CODE,
    CONFIG_DATA,
    CREDENTIALS,
    NAME,
    PROVIDER_CODE,
    PROVIDER_NAME,
    STATUS,
    VALUE,
)
from src.specs.enums.provider import Providers
from src.specs.enums.status import Status
from src.specs.helpers.common import get_routes_list

from corefw.appfw.routes import apikeys_ns, integration_ns
from corefw.enums.provider import Providers

CREATE_APIKEY_MODEL = apikeys_ns.model(
    "apikeys_model",
    {
        NAME: fields.String(required=True),
        ASSOCIATED_GROUPS: fields.List(
            fields.String(), min_items=1, required=True, unique=True
        ),
    },
)
UPDATE_APIKEY_MODEL = apikeys_ns.model("update_apikey", {STATUS: fields.String()})

CREATE_GROUP_MODEL = apikeys_ns.model(
    "create_api_group",
    {
        NAME: fields.String(required=True),
        ASSOCIATED_APPS: fields.List(
            fields.String(),
            min_items=1,
            required=True,
            unique=True,
            example=get_routes_list(),
        ),
    },
)

CREATE_APIKEY_SUCCESS = apikeys_ns.model(
    "create_apikey_success", {API_KEY: fields.String()}
)

CREATE_VLS_APIKEY_MODEL = apikeys_ns.model(
    "vls_apikeys_model",
    {
        API_KEY: fields.String(required=True),
        CLIENT_CODE: fields.String(required=True),
        CLIENT: fields.String(required=True),
    },
)

CREDENTIALS_MODEL = integration_ns.model(
    "credentials_model",
    {
        NAME: fields.String(required=True, min_length=5),
        VALUE: fields.String(required=True, min_length=10),
    },
)

CREATE_INTEGRATION = integration_ns.model(
    "integration_post_model",
    {
        PROVIDER_CODE: fields.String(
            required=True,
            enum=Providers.values(),
            example=(",".join([row for row in Providers.values()])),
        ),
        PROVIDER_NAME: fields.String(required=True),
        CONFIG_DATA: fields.Nested(
            model=integration_ns.model("config_model", {}), required=True
        ),
        CREDENTIALS: fields.List(fields.Nested(model=CREDENTIALS_MODEL), min_items=1),
    },
)

UPDATE_INTEGRATION = integration_ns.model(
    "integration_update_model",
    {
        STATUS: fields.String(
            enum=Status.values(), example=(",".join([row for row in Status.values()]))
        ),
        CONFIG_DATA: fields.Nested(
            model=integration_ns.model("config_model", {}), required=True
        ),
        CREDENTIALS: fields.List(fields.Nested(model=CREDENTIALS_MODEL), min_items=1),
    },
)
