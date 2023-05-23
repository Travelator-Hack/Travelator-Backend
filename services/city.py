from pydantic import BaseModel
from .database import _MongoClient

class City(BaseModel):
    id: str
    name: str


class City_Service(_MongoClient):
    def __init__(self) -> None:
        super().__init__()
        self.cities_collection = self.db['cities']

    async def _exists(self, name: str) -> bool:
        return bool(await self.cities_collection.findOne({'title': name}))

    async def find_city_by_name(self, name) -> City:
        return await self.cities_collection.find({'title': name}, {'title': 1})
    
    