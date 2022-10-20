from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.command_cursor import CommandCursor

from .base import BasePersistentClient
from api import settings


class MongoDbClient(BasePersistentClient):

    def __init__(self, mongo_uri: str):
        self.mongo_uri = mongo_uri
        self.client: MongoClient = self._connect()

    def _connect(self):
        return MongoClient(self.mongo_uri)

    def _use_database(self, database: str) -> Database:
        return Database(self.client, database)

    def _execute_query_one(self):
        pass

    def _execute_query_all(self):
        pass


    def get_quiz(
        self
    ):
        db: Database = self._use_database(settings.MONGODB_MASTER_DB_NAME)
        collection: Collection = Collection(db, "--")
        data: CommandCursor = collection.aggregate([
           
        ])

        return data

    def get_aggregated_by_hour_traffic_reach_summary(
        self, start_date, end_date, locations, country, radius=200
    ):
        pass
    
