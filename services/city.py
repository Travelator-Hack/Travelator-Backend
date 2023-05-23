from pydantic import BaseModel
from .database import _MongoClient

class City:
    id: str
    ya_id: str
    name: str
    country: str
    description: str
    coordinates: tuple(float, float)
    rating: int


class City_Service(_MongoClient):
    def __init__(self) -> None:
        super().__init__()
        self.cities_collection = self.db['cities']
        # self.events = self.db.cities.events # События 
        # self.excursions = self.db.excursions # Экскурсии
        # self.hotels = self.db.hotels # Отели
        # self.places = self.db.places # Достопримечательности 
        # self.restaurants = self.db.restaurants # Рестораны

    async def _exists(self, name: str) -> bool:
        return bool(await self.cities_collection.findOne({'title': name}))

    