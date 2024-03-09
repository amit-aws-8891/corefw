from flask import current_app
from pymongo.errors import DuplicateKeyError

from corefw import get_settings
from corefw.exceptionsfw.exceptions import DataBaseException
from corefw.loggerfw.logger import get_logger
from corefw.mongofw.mongo_client import MongoClient

LOGGER = get_logger(__name__)


class DataAccessObject:
    """
    Data access layer
    """

    def __init__(self, db_name=None, mongo_url=None, collection_name=None):
        mongo_url = mongo_url if mongo_url else self.get_mongo_url()
        db_name = db_name if db_name else self.get_db_name()
        self.db_name = db_name
        self.mongo_conn = MongoClient(mongo_url=mongo_url, db_name=db_name)
        self.collection_name = collection_name
        if not collection_name:
            self.collection_name = get_settings(current_app, "APIKEY_COLLECTION")


    def get_db_name(self):
        """
        Get db name
        :return:
        """
        db_name = "veefin_gateway"
        if current_app.config["DB_NAME"]:
            db_name = current_app.config["DB_NAME"]
        return db_name

    def get_mongo_url(self):
        """
        Get Mongo URL here
        :return:
        """
        mongo_url = "localhost:27017"
        if current_app.config["MONGO_URL"]:
            mongo_url = current_app.config["MONGO_URL"]
        return mongo_url

    def get_connection(self):
        """
        Get mongo connection
        """
        if self.mongo_conn.get_connection():
            return True
        return False

    def count(self, filter_dict, collection_name=None):
        """
        Get count
        """
        collection_name = collection_name if collection_name else self.collection_name
        try:
            count = self.mongo_conn.count(
                collection_name=collection_name, query_filter=filter_dict
            )
            return count
        except BaseException as ex:  # NOSONAR
            LOGGER.error(ex)
            raise DataBaseException(message=ex)

    def get_resource(self, filter_dict, collection_name=None, project_fields=None):
        """
        Get Resource using filter
        """
        try:
            if not project_fields:
                project_fields = {"_id": 0}
            record = self.mongo_conn.find_one(
                filter=filter_dict,
                collection_name=collection_name
                if collection_name
                else self.collection_name,
                project_fields=project_fields,
            )
            return record
        except BaseException as ex:  # NOSONAR
            LOGGER.error(ex)
            raise DataBaseException(message=ex)

    def find_all_with_collation(
        self, filter_dict, sort_by, collection_name=None, **kwargs
    ):
        """
        Get list here
        """

        try:
            records = []
            collection_name = (
                collection_name if collection_name else self.collection_name
            )
            mongo_conn = self.mongo_conn.get_connection()
            cursor = (
                mongo_conn[self.db_name][collection_name]
                .find(filter_dict, kwargs.get("project_fields", {"_id": 0}))
                .collation(kwargs.get("collation", {"locale": "en"}))
                .sort([(sort_by, kwargs.get("direction", 1))])
                .skip(kwargs.get("offset", 0))
                .limit(kwargs.get("limit", 500))
            )

            for row in cursor:
                records.append(row)
            return records
        except BaseException as ex:  # NOSONAR
            LOGGER.error(ex)
            raise DataBaseException(message=str(ex))

    # @log
    def create(self, data, db_name=None):
        """
        Create a new resource
        @return:
        """
        db_name = db_name if db_name else self.db_name
        try:
            # if not self.mongo_client.db_exists(self.db_name):
            # self.create_indexes()
            resource_id = self.mongo_conn.create(
                db_name=db_name, collection_name=self.collection_name, content=data
            )
            return resource_id
        except DuplicateKeyError as dup_err:
            LOGGER.error(dup_err)
            raise DataBaseException(message=dup_err.details["errmsg"])
        except BaseException as error_string:  # NOSONAR
            LOGGER.error(error_string)
            raise DataBaseException(message=error_string)

    def update(
        self, data, filter_dict: dict, update_content_type="$set", collection_name=None
    ):
        """
        @param data:
        @param filter_dict:
        @param update_content_type
        @return:
        """
        collection_name = collection_name if collection_name else self.collection_name
        try:
            self.mongo_conn.find_one_and_update(
                collection_name=collection_name,
                filter=filter_dict,
                update_content={update_content_type: data},
            )
        except DuplicateKeyError as ex:
            LOGGER.error(ex)
            raise DataBaseException(message="Duplicate key")
        except BaseException as error_string:  # NOSONAR
            LOGGER.error(error_string)
            raise DataBaseException(message=error_string)

    def create_indexes(self, indexes, collection_name=None):
        """
        Creating Index on indexes fields individually as uniqueness True
        :return:
        """
        collection_name = collection_name if collection_name else self.collection_name
        for index in indexes:
            try:
                self.mongo_conn.create_index_key(
                    collection_name=collection_name,
                    indexname=index.get("indexname"),
                    field_name=index.get("field_name"),
                    uniqueness=index.get("is_unique"),
                )
            except BaseException as base_exception:  # NOSONAR
                LOGGER.error(base_exception)
                raise DataBaseException(message=base_exception)

    def create_indexes_raw(self, indexes, unique=False, collection_name=None):
        """
        Creating Index on indexes fields individually as uniqueness True
        :return:
        """
        collection_name = collection_name if collection_name else self.collection_name

        try:
            self.mongo_conn.create_index_raw(
                collection_name=collection_name, keys=indexes, uniqueness=unique
            )
        except BaseException as base_exception:  # NOSONAR
            LOGGER.error(base_exception)
            raise DataBaseException(message=base_exception)

    def delete(self, filter_dict: dict, collection_name=None):
        """
        Delete a resource
        @param filter_dict:
        @param collection_name:
        @return:
        """
        collection_name = collection_name if collection_name else self.collection_name
        try:
            self.mongo_conn.delete_one(
                collection_name=collection_name, filter=filter_dict
            )
        except BaseException as exception:  # NOSONAR
            LOGGER.error(exception)
            raise DataBaseException(message=exception)
