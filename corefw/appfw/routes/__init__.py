from flask_restx import Namespace

health_ns = Namespace(name="health api", description="Health Api")
apikeys_ns = Namespace(
    name="Internal API Keys api", description="Internal Api Keys Apis"
)
integration_ns = Namespace(name="Integrations", description="Integrations")
