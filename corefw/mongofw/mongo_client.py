import logging
from datetime import datetime, timedelta

import pymongo
from pymongo.collection import ReturnDocument

LOGGER = logging.getLogger(__name__)


class MongoClient(object):
    def __init__(self, mongo_url, db_name):
        self.mongo_connection = None
        self.tenant_info = None
        self.mongo_url = mongo_url
        self.db_name = db_name

    def get_connection(self):
        """Get the connection to mongo db

        :return: the client to connect to mongodb
        """
        try:
            self.mongo_connection = pymongo.MongoClient(
                self.mongo_url, serverSelectionTimeoutMS=2000
            )
            return self.mongo_connection
        except pymongo.errors.ServerSelectionTimeoutError as timeoutEx:
            print(timeoutEx)
            return False

    def create(self, collection_name, content, db_name=None, session=None):
        """Insert a single document.

        :param db_name: Database name to be inserted, if not exist, will be
        added automatically
        :param collection_name: Collection name to be inserted, if not exist,
        will be added automatically
        :param content: the document content in json to be inserted.
        Ex: {'x': 1}
        :param session: for database transactions
        :return: The inserted document id. Ex:'doc id'
        """
        if not db_name:
            db_name = self.db_name
        mongo_conn = self.get_connection()
        result = mongo_conn[db_name][collection_name].insert_one(
            content, session=session
        )
        return result.inserted_id

    def create_many(self, db_name, collection_name, content, session=None):
        """Insert a single document.
        :param db_name: Database name to be inserted, if not exist, will be added automatically
        :param collection_name: Collection name to be inserted, if not exist,
        will be added automatically
        :param content: an array of the document content in json to be inserted.
        Ex: [{'x': 1}, {y:2}]
        :param session: for database transactions
        :return: The inserted document id. Ex:'doc id'
        """

        mongo_conn = self.get_connection()
        return mongo_conn[self.get_tenant_db(db_name)][collection_name].insert_many(
            content, session=session
        )

    def find_one_and_update(
        self,
        collection_name,
        filter,
        update_content,
        project_fields=None,
        get_mongo_doc_id=False,
        upsert=False,
        array_filters=None,
        db_name=None,
        session=None,
    ):
        """Finds a single document and updates it

        :param project_fields:
        :param db_name:Database name to be inserted, if not exist, will be
        added automatically
        :param collection_name:Collection name to be inserted, if not exist,
        will be added automatically
        :param filter: json to filter the document. Ex: {'userid': '123'}
        :param update_content: json format for update content.
        Ex: {'$set': {'done': True}}
        :param project_fields: A list of field names that should be returned
        in the result document or a mapping specifying
        the fields
        :param get_mongo_doc_id: When ``True``, adds the ``_id`` field to
        ``project_fields``
        :param upsert: When ``True``, inserts a new document if no
        document matches the query
        :param array_filters: A list of filters specifying which
        array elements an update should apply.
        :param session: for database transactions
        :return: updated document
        """

        if not db_name:
            db_name = self.db_name

            if project_fields is None:
                project_fields = {"_id": 0}
        mongo_conn = self.get_connection()
        return mongo_conn[db_name][collection_name].find_one_and_update(
            filter,
            update_content,
            return_document=ReturnDocument.AFTER,
            projection=project_fields,
            upsert=upsert,
            array_filters=array_filters,
            session=session,
        )

    def update_many(
        self,
        db_name,
        collection_name,
        query_filter,
        update_content,
        upsert=False,
        array_filters=None,
        session=None,
    ):
        """Finds multiple documents and updates these documents

        :param db_name:Database name to be inserted, if not exist, will be
        added automatically
        :param collection_name:Collection name to be inserted, if not exist,
        will be added automatically
        :param query_filter: json to filter the document. Ex: {'userid': '123'}
        :param update_content: json format for update content.
        Ex: {'$set': {'done': True}}
        :param upsert: When ``True``, inserts a new document if no
        document matches the query
        :param array_filters: A list of filters specifying which
        array elements an update should apply.
        :param session: for database transactions
        :return: An instance of :class:`~pymongo.results.UpdateResult`
        """

        mongo_conn = self.get_connection()
        return mongo_conn[self.get_tenant_db(db_name)][collection_name].update_many(
            query_filter,
            update_content,
            upsert=upsert,
            array_filters=array_filters,
            session=session,
        )

    def find_one(self, collection_name, filter, db_name=None, project_fields=None):
        """Get a single document from the database.

        :param db_name: Database name to be inserted, if not exist, will be
        added automatically
        :param collection_name: Collection name to be inserted, if not exist,
        will be added automatically
        :param filter: json to filter the document. Ex: {'userid': '123'}
        :param project_fields: a dict of field names that should be returned in
        the result set or a dict
        :return: found document
        """
        if not db_name:
            db_name = self.db_name
        if project_fields is None:
            project_fields = {}
        project_fields["_id"] = 0
        mongo_conn = self.get_connection()
        return mongo_conn[db_name][collection_name].find_one(filter, project_fields)

    def find_all(
        self,
        collection_name,
        filter=None,
        project_fields=None,
        skip=0,
        limit=500,
        sort_by=None,
        direction=None,
        db_name=None,
        get_mongo_doc_id=False,
    ):
        """Query the documents list in database.

        :param db_name:Database name to be inserted, if not exist, will be
        added automatically
        :param collection_name: Collection name to be inserted, if not exist,
        will be added automatically
        :param filter: json to filter the document. Ex: {'userid': '123'}
        :param project_fields: a dict of field names that should be returned in
        the result set or a dict
        specifying the fields. Ex: {'_id': 0,'name':1}
        :param skip: offset to start retrieve document. Ex:100 , default=0
        :param limit: the number of document to be return. Ex10, default=500
        :param sort_by: offset to start retrieve document. Ex:100 , default=0
        :param direction: Sort order. ASCENDING = 1 and DESCENDING = -1
        :return: list of documents
        """
        if not db_name:
            db_name = self.db_name
        mongo_conn = self.get_connection()
        if project_fields is None:
            project_fields = {}
        project_fields["_id"] = 0

        if sort_by and direction:
            return (
                mongo_conn[db_name][collection_name]
                .find(filter, project_fields)
                .sort([(sort_by, direction)])
                .skip(skip)
                .limit(limit)
            )

        return (
            mongo_conn[db_name][collection_name]
            .find(filter, project_fields)
            .skip(skip)
            .limit(limit)
        )

    def delete_one(self, collection_name, filter, db_name=None, session=None):
        """Delete a single document matching the filter.

        :param db_name:Database name to be inserted, if not exist, will be
        added automatically
        :param collection_name: Collection name to be inserted, if not exist,
        will be added automatically
        :param filter: json to filter the document. Ex: {'userid': '123'}
        :param session: for database transactions
        :return: Number of deleted document. Ex:1
        """

        mongo_conn = self.get_connection()
        result = mongo_conn[db_name][collection_name].delete_one(
            filter, session=session
        )
        return result.deleted_count

    def delete_many(self, db_name, collection_name, search_filter, session=None):
        """Delete a many documents matching the search_filter.

        :param db_name:Database name to be inserted, if not exist, will be
        added automatically
        :param collection_name: Collection name to be inserted, if not exist,
        will be added automatically
        :param search_filter: json to filter the document.
        Ex: {'status': 'failed'}
        :param session: for database transactions
        :return: Number of deleted document. Ex:5
        """

        mongo_conn = self.get_connection()
        result = mongo_conn[self.get_tenant_db(db_name)][collection_name].delete_many(
            search_filter, session=session
        )
        return result.deleted_count

    def find_one_and_replace(
        self,
        db_name,
        collection_name,
        query_filter,
        update_content,
        upsert=True,
        session=None,
    ):
        """Finds a single document and replace it

        :param db_name:Database name to be inserted, if not exist, will be
        added automatically
        :param collection_name:Collection name to be inserted, if not exist,
        will be added automatically
        :param query_filter: json to filter the document. Ex: {'userid': '123'}
        :param update_content: json format for update content
        :param upsert: insert if document isn't exists
        :param session: for database transactions
        :return: result of inserted document
        """

        mongo_conn = self.get_connection()
        return mongo_conn[self.get_tenant_db(db_name)][collection_name].replace_one(
            query_filter, update_content, upsert=upsert, session=session
        )

    def save(self, db_name, collection_name, document):
        """Insert or update document by matching _id field

        :param db_name:Database name to be inserted, if not exist, will be
        added automatically
        :param collection_name:Collection name to be inserted, if not exist,
        will be added automatically
        :param document: document to be inserted or updated
        :return: result of inserted document
        """

        mongo_conn = self.get_connection()
        return mongo_conn[self.get_tenant_db(db_name)][collection_name].save(document)

    def db_exists(self, db_name):
        """check whether database exists or not

        :param db_name:Database name to be inserted, if not exist, will be
        added automatically
        :return: true if database exists
        """

        mongo_conn = self.get_connection()
        db_names = mongo_conn.list_database_names()

        if db_name in db_names:
            return True

        return False

    def aggregate(self, db_name, collection_name, query_fitler, allow_disk_use=False):
        """

        :param db_name:Database name to be inserted, if not exist, will be
        added automatically
        :param collection_name:Collection name to be inserted, if not exist,
        will be added automatically
        :param query_fitler: json to filter the document. Ex: {'userid': '123'}
        :return: result of inserted document
        """

        mongo_conn = self.get_connection()
        return mongo_conn[db_name][collection_name].aggregate(
            query_fitler, allowDiskUse=allow_disk_use
        )

    def create_index(self, collection_name, keys, indexname, uniqueness, db_name=None):
        """

        :param db_name:Database name to be inserted, if not exist, will be
        added automatically
        :param collection_name:Collection name to be inserted, if not exist,
        will be added automatically
        :param keys: list of keys we need to create an index on
        eg:[('context.contexttagtype', 'text')]
        :param indexname: name of the index
        :param uniqueness: True/False
        :return: result of inserted document
        """
        if not db_name:
            db_name = self.db_name
        mongo_conn = self.get_connection()
        return mongo_conn[db_name][collection_name].create_index(
            keys, name=indexname, unique=uniqueness, background=True
        )

    def create_index_raw(self, collection_name, keys, uniqueness, db_name=None):
        if not db_name:
            db_name = self.db_name
        mongo_conn = self.get_connection()
        return mongo_conn[db_name][collection_name].create_index(
            keys, unique=uniqueness, background=True
        )

    def create_index_key(
        self,
        field_name,
        indexname,
        uniqueness,
        sparse=True,
        collection_name=None,
        db_name=None,
    ):
        """

        :param db_name:Database name to be inserted, if not exist, will be
        added automatically
        :param collection_name:Collection name to be inserted, if not exist,
        will be added automatically
        :param field_name: field_name
        :param keys: list of keys we need to create an index on
        eg:[('context.contexttagtype', 'text')]
        :param indexname: name of the index
        :param uniqueness: True/False
        :return: result of inserted document
        """
        db_name = db_name if db_name else self.db_name
        collection_name = collection_name if collection_name else self.collection_name
        mongo_conn = self.get_connection()

        if indexname not in mongo_conn[db_name][collection_name].index_information():
            return mongo_conn[db_name][collection_name].create_index(
                field_name,
                name=indexname,
                unique=uniqueness,
                sparse=sparse,
                background=True,
            )

        return indexname

    def count(self, collection_name, query_filter=None, db_name=None):
        """
        Gets record's count

        :param db_name:Database name to be inserted, if not exist, will be
        added automatically
        :param collection_name:Collection name to be inserted, if not exist,
        will be added automatically
        :param query_filter: json to filter the document. Ex: {'userid': '123'}
        :return: result of inserted document
        """
        db_name = db_name if db_name else self.db_name
        client = self.get_connection()

        if query_filter:
            return client[db_name][collection_name].count(query_filter)

        return client[db_name][collection_name].count()

    def distinct(self, db_name, collection_name, field, query_filter=None):
        """

        :param db_name: Database name from which the values to be retrieved
        :param collection_name: Collection name from which the values to be
        retrieved
        :param field: The field for which to return distinct values.
        :param query_filter: A query that specifies the documents from which to
        retrieve
        the distinct values.
        :return: distinct value for the field
        """

        mongo_conn = self.get_connection()
        return mongo_conn[db_name][collection_name].distinct(field, query_filter)

    def delete_database(self, db_name):
        """
        Method to delete a database
        :param db_name: Database name to be deleted
        :return: boolean
        """

        mongo_conn = self.get_connection()
        return mongo_conn.drop_database(self.get_tenant_db(db_name))

    def release_lock(self, lock_id, **kwargs):
        """
        Release a lock.

        :param lock_id: a string indentifying the lock
        :key db_name: name of the locks database
        :key collection_name: name of the locks collection
        :return: True if release was successful, False otherwise
        """

        db_name = kwargs.get("db_name", "locks")
        collection_name = kwargs.get("collection_name", "active_locks")
        client = self.get_connection()
        col = client[self.get_tenant_db(db_name)][collection_name]

        result = col.delete_one({"_id": lock_id})
        return True if result.deleted_count == 1 else False

    def touch_lock(self, lock_id, expires_in=4, **kwargs):
        """
        Touch a lock by updating its expiration.

        :param lock_id: a string indentifying the lock
        :param expires_in: how many seconds from now to expire the lock
        :key db_name: name of the locks database
        :key collection_name: name of the locks collection
        :return: True if lock update was successful, False otherwise
        """

        db_name = kwargs.get("db_name", "locks")
        collection_name = kwargs.get("collection_name", "active_locks")
        client = self.get_connection()
        col = client[self.get_tenant_db(db_name)][collection_name]
        expire = datetime.utcnow() + timedelta(seconds=expires_in)

        result = col.update_one({"_id": lock_id}, {"$set": {"expire": expire}})
        return True if result.modified_count == 1 else False
