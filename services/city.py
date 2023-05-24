from pydantic import BaseModel
from .database import _MongoClient

class Events(BaseModel):
    id: str
    title: str
    age: str
    start_date: str | None
    end_date: str | None
    ticket_price: str
    is_avaible: bool 
    city_id: str
    description: str 

class EventsRetrieve(BaseModel):
    pass

class Excursions(BaseModel):
    id: str
    title: str
    age: str
    has_audio_guide: bool
    language: list[str]
    ticket_price: str
    is_avaible: bool
    city_id: str
    description: str
    route: dict[str, str]

class ExcursionsRetrieve(BaseModel):
    pass


class Hotels(BaseModel):
    id: str
    title: str
    
    city_id: str
    description: str

class HotelsRetrieve(BaseModel):
    pass

class Places(BaseModel):
    id: str
    title: str
    
    city_id: str
    description: str

class PlacesRetrieve(BaseModel):
    pass


class Restaurant(BaseModel):
    id: str
    title: str
    
    city_id: str
    description: str

class RestaurantRetrieve(BaseModel):
    pass


class City(BaseModel):
    id: str
    title: str
    

class City_Service(_MongoClient):
    def __init__(self) -> None:
        super().__init__()
        self.cities_collection = self.db['cities']

    async def _exists(self, title: str) -> bool:
        return bool(await self.cities_collection.findOne({'title': title}))

    async def find_city_by_title(self, title) -> City:
        return await self.cities_collection.find({'title': title}, {'title': 1})
    
    