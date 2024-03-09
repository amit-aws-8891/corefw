from flask import request
from flask_restx import Resource, reqparse

from corefw.appfw.routes import apikeys_ns
from corefw.appfw.services.apikeys_services import ApiKeysService
from corefw.authfw.internal_auth import internal_auth
from corefw.constants.constants import API_KEY, CODE, MESSAGE
from corefw.constants.messages import (
    API_KEY_CREATED,
    BAD_REQUEST,
    FORBIDDEN,
    GROUP_CREATED,
)
from corefw.constants.urls import APIK_GROUP_URL, APIKEYS_URL
from corefw.models.v1.request_model import CREATE_APIKEY_MODEL, CREATE_GROUP_MODEL

api_key_routes_parser = reqparse.RequestParser()


@apikeys_ns.route(APIKEYS_URL)
class APIKeysRoutes(Resource):
    """
    APIKeys management
    """

    api_key_routes_parser.add_argument("x-api-key", location="headers", required=True)

    @apikeys_ns.response(403, description=FORBIDDEN)
    @apikeys_ns.response(400, description=BAD_REQUEST)
    @apikeys_ns.expect(CREATE_APIKEY_MODEL, api_key_routes_parser, validate=True)
    @internal_auth
    def post(self):
        """
        Create API keys
        docs: To create master key add associated_groups = ["*"]
        :return:
        """
        # ** request.get_json()
        result, status = ApiKeysService().create_api_key(**request.get_json())
        response = {API_KEY: result, MESSAGE: API_KEY_CREATED}
        return response, status


@apikeys_ns.route(APIK_GROUP_URL)
class APIGroupRoutes(Resource):
    """
    APIKeys management
    """

    api_key_routes_parser.add_argument("x-api-key", location="headers", required=True)

    @apikeys_ns.response(403, description=FORBIDDEN)
    @apikeys_ns.response(400, description=BAD_REQUEST)
    @apikeys_ns.expect(api_key_routes_parser, validate=True)
    @internal_auth
    def get(self):
        """
        Get API Group list
        :return:
        """
        result, status = ApiKeysService().get_group_list()
        return result, status

    # @apikeys_ns.response(200, model=CREATE_APIKEY_SUCCESS, description=SUCCESS)

    @apikeys_ns.response(403, description=FORBIDDEN)
    @apikeys_ns.response(400, description=BAD_REQUEST)
    @apikeys_ns.expect(CREATE_GROUP_MODEL, api_key_routes_parser, validate=True)
    @internal_auth
    def post(self):
        """
        Create API Group
        :return:
        """
        # ** request.get_json()
        result, status = ApiKeysService().create_group(**request.get_json())
        response = {MESSAGE: GROUP_CREATED[1], CODE: GROUP_CREATED[0]}
        return response, status
