from flask_restx import Resource

from corefw.appfw.routes import health_ns
from corefw.loggerfw import logger

logger = logger.get_logger(__name__)


@health_ns.route("health")
class Health(Resource):
    def get(self):
        logger.info("Health")
        return {"message": "Success"}, 200


@health_ns.route("mongohealth")
class MongoHealth(Resource):
    def get(self):
        logger.info("check health")
        logger.critical("error check health")
        return {"message": "Success"}, 200
