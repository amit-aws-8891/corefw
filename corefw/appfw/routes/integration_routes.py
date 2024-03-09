from flask import request
from flask_restx import Resource, reqparse

from corefw.appfw.routes import integration_ns
from corefw.appfw.services.integration_services import IntegrationService
from corefw.constants.constants import MESSAGE
from corefw.constants.messages import BAD_REQUEST, FORBIDDEN
from corefw.constants.urls import (
    INTEGRATION_DETAILS_URL,
    INTEGRATION_URL,
    SANDBOX_INTEGRATION_DETAILS_URL,
    SANDBOX_INTEGRATION_URL,
)
from corefw.models.v1.request_model import CREATE_INTEGRATION, UPDATE_INTEGRATION

integration_parser = reqparse.RequestParser()


@integration_ns.route(INTEGRATION_URL)
class Integration(Resource):
    """
    Vendor integration
    """

    integration_parser.add_argument("x-api-key", location="headers", required=True)

    @integration_ns.response(403, description=FORBIDDEN)
    @integration_ns.response(400, description=BAD_REQUEST)
    @integration_ns.expect(CREATE_INTEGRATION, integration_parser, validate=True)
    def post(self):
        """
        Create Integrations
        :return:
        """
        # ** request.get_json()
        result, status = IntegrationService().create_integration(**request.get_json())
        response = {MESSAGE: result}
        return response, status


@integration_ns.route(INTEGRATION_DETAILS_URL)
class IntegrationDetails(Resource):
    """
    Vendor integration
    """

    integration_parser.add_argument("x-api-key", location="headers", required=True)

    @integration_ns.response(403, description=FORBIDDEN)
    @integration_ns.response(400, description=BAD_REQUEST)
    @integration_ns.expect(integration_parser, validate=True)
    def get(self, provider_code):
        """
        Get Integrations by provider_code
        :return:
        """
        # ** request.get_json()
        result, status = IntegrationService().get_integration(provider_code)
        return result, status

    @integration_ns.response(403, description=FORBIDDEN)
    @integration_ns.response(400, description=BAD_REQUEST)
    @integration_ns.expect(UPDATE_INTEGRATION, integration_parser, validate=True)
    def patch(self, provider_code):
        """
        Update Integrations by provider_code
        :return:
        """
        # ** request.get_json()
        result, status = IntegrationService().update_integration(
            provider_code, **request.get_json()
        )
        response = {MESSAGE: result}
        return response, status

    @integration_ns.response(403, description=FORBIDDEN)
    @integration_ns.response(400, description=BAD_REQUEST)
    @integration_ns.expect(integration_parser, validate=True)
    def delete(self, provider_code):
        print(provider_code)
        IntegrationService().delete_integration(provider_code)
        return {}, 204


@integration_ns.route(SANDBOX_INTEGRATION_URL)
class SandboxIntegration(Resource):
    """
    Vendor integration
    """

    integration_parser.add_argument("x-api-key", location="headers", required=True)

    @integration_ns.response(403, description=FORBIDDEN)
    @integration_ns.response(400, description=BAD_REQUEST)
    @integration_ns.expect(CREATE_INTEGRATION, integration_parser, validate=True)
    def post(self):
        """
        Create sandbox Integrations
        :return:
        """
        result, status = IntegrationService().create_sandbox_integration(
            **request.get_json()
        )
        response = {MESSAGE: result}
        return response, status


@integration_ns.route(SANDBOX_INTEGRATION_DETAILS_URL)
class SandboxIntegrationDetails(Resource):
    """
    Vendor integration
    """

    integration_parser.add_argument("x-api-key", location="headers", required=True)

    @integration_ns.response(403, description=FORBIDDEN)
    @integration_ns.response(400, description=BAD_REQUEST)
    @integration_ns.expect(integration_parser, validate=True)
    def get(self, provider_code):
        """
        get sandbox Integrations
        :return:
        """
        # ** request.get_json()
        result, status = IntegrationService().get_sandbox_integration(provider_code)
        return result, status

    @integration_ns.response(403, description=FORBIDDEN)
    @integration_ns.response(400, description=BAD_REQUEST)
    @integration_ns.expect(UPDATE_INTEGRATION, integration_parser, validate=True)
    def patch(self, provider_code):
        """
        update sandbox Integrations
        :return:
        """
        # ** request.get_json()
        result, status = IntegrationService().update_integration(
            provider_code, **request.get_json()
        )
        response = {MESSAGE: result}
        return response, status

    @integration_ns.response(403, description=FORBIDDEN)
    @integration_ns.response(400, description=BAD_REQUEST)
    @integration_ns.expect(integration_parser, validate=True)
    def delete(self, provider_code):
        IntegrationService().delete_integration(provider_code)
        return {}, 204
