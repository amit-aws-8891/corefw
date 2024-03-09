from flask import Flask
from flask_restx import Api

from corefw.appfw.routes import (
    api_keys_routes,
    apikeys_ns,
    health_ns,
    health_routes,
    integration_ns,
    integration_routes,
)
from corefw.constants.constants import API_PREFIX


def initialize_app(title, description, version, config_val, is_doc=True):
    """
    Initializing app here
    :return: app, api
    """
    app = Flask(__name__)
    authorizations = {"apikey": {"type": "apiKey", "in": "header", "name": "x-api-key"}}
    api = Api(
        app,
        authorizations=authorizations,
        security="apikey",
        version=version,
        title=title,
        description=description,
        doc=is_doc,
    )
    app.config.update(config_val)
    api.add_namespace(health_ns, path="/")
    api.add_namespace(health_ns, path="/")
    api.add_namespace(apikeys_ns, path=API_PREFIX)
    api.add_namespace(integration_ns, path=API_PREFIX)
    return app, api
