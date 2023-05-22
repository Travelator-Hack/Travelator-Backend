import os
import typing as tp
from loguru import logger

from motor.motor_asyncio import AsyncIOMotorClient

class _MongoClient:
    def __init__(self) -> None:
        _url = os.environ.get('MONGO_CONN_STR')
        logger.info(f'Connecting to MongoDB at {_url}')

        self.mongo = AsyncIOMotorClient(_url)['db']

    @property
    def db(self):
        """Get mongo client connected to db."""
        return self.mongo
    

MongoClient = _MongoClient()
