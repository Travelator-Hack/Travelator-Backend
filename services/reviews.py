from datetime import datetime
from schemas.review import ReviewCreation, ReviewRetrieve, ReviewType
from services.database import _MongoClient


class _ReviewsService(_MongoClient):
    def __init__(self, url: str | None = None) -> None:
        super().__init__(url)
        self.coll = self.db['reviews']

    async def _exists(self, username: str, type_: ReviewType) -> bool:
        return bool(await self.coll.find_one({'username': username, 'type': type_}))
    
    async def get_user_reviews(self, username: str) -> list[ReviewRetrieve]:
        cursor = self.coll.find({'username': username})
        return list(map(ReviewRetrieve.from_dict, await cursor.to_list(length=None))) # type: ignore
    
    async def create_review(self, data: ReviewCreation, username: str) -> None:
        if await self._exists(username, data.type):
            raise ValueError('User already posted review')
        now = datetime.now()
        await self.coll.insert_one({**data.dict(), 'username': username, 'ts_created': now})

    async def get_entities_reviews(self, entity: ReviewType, id_: str):
        cursor = self.coll.find({'type': entity, 'entity_id': id_})
        return list(map(ReviewRetrieve.from_dict, await cursor.to_list(length=None))) # type: ignore


ReviewsService = _ReviewsService()
