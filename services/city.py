from pydantic import BaseModel
from .database import _MongoClient
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection


class Event(BaseModel):
    id: str
    title: str
    age: str
    start_date: str | None
    end_date: str | None
    ticket_price: str
    is_available: bool
    city_id: str
    description: str


class EventRetrieve(BaseModel):
    pass


class Excursion(BaseModel):
    id: str
    title: str
    age: str
    has_audio_guide: bool
    language: list[str]
    form: str | None
    duration_hours: str
    ticket_price: str
    is_available: bool
    city_id: str
    description: str
    program: str
    route: dict[str, str]


class ExcursionRetrieve(BaseModel):
    pass


class Hotel(BaseModel):
    id: str
    title: str
    address: str
    email: str
    phones: list[str]
    activities: dict[str, str]
    rooms: dict[str, bool]
    meals: list[str]
    services: list[dict[str, str]]
    city_id: str
    stars: str
    description: str


class HotelsRetrieve(BaseModel):
    pass


class Place(BaseModel):
    id: str
    title: str
    address: str


    city_id: str
    description: str


class PlaceRetrieve(BaseModel):
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
    events: list[Event]
    excursions: list[Excursion]
    hotels: list[Hotel]
    places: list[Place]
    restaurants: list[Restaurant]


class _CityService(_MongoClient):
    def __init__(self) -> None:
        super().__init__()
        self.cities_collection = self.db["cities"]
        self.regions_collection = self.db["regions"]
        self.events_collection = self.db["events"]
        self.excursions_collection = self.db["excursions"]
        self.hotels_collection = self.db["hotels"]
        self.places_collection = self.db["places"]
        self.restaurants_collection = self.db["restaurants"]

    def _parse_list(self, data: dict):
        _id = str(data.pop("_id"))
        return {**data["dictionary_data"], "id": _id}

    async def _exists(self, title: str) -> bool:
        return bool(await self.cities_collection.find_one({"title": title}))

    async def list_regions(self):
        return list(
            map(
                self._parse_list,
                await self.regions_collection.find({}, {"dictionary_data.title": 1, "_id": 1}).to_list(length=86),  # type: ignore
            )
        )

    async def find_region_by_id(self, _id: str):
        region = await self.regions_collection.find_one({"_id": ObjectId(_id)})
        if not region:
            raise ValueError("Region not found")
        return self._parse_list(region)  # type: ignore
        # _id = str(region.pop("_id"))
        # return {**region, 'id': _id}

    async def find_cities_by_region_id(self, region_id: str):
        return list(
            map(
                self._parse_list,
                await self.cities_collection.find({"dictionary_data.region": region_id}).to_list(length=3000),  # type: ignore
            )
        )

    async def find_city_by_id(self, _id: str):
        city = await self.cities_collection.find_one({"_id": ObjectId(_id)})
        if not city:
            raise ValueError("City not found")
        _id = str(city.pop("_id"))  # type: ignore
        return {**city, "id": _id}

    async def list_cities(self):
        return list(
            map(
                self._parse_list, (await self.cities_collection.find({}, {"dictionary_data.title": 1, "_id": 1}).to_list(length=None))  # type: ignore
            )
        )
    
    async def find_events_by_city_id(self, city_id: str):
        return list(
            map(
            self._parse_list,
            await self.events_collection.find({"dictionary_data.city": city_id}, {
                "_id": 1,
                "dictionary_data.title": 1#,
                # "dictionary_data.age": 1,
                # "dictionary_data.timetable_by_place.schedule.start": 1,
                # "dictionary_data.timetable_by_place.schedule.end": 1,
                # "dictionary_data.ticket_price": 1,
                # "dictionary_data.is_can_buy": 1,
                # "dictionary_data.city": 1,
                # "dictionary_data.description": 1
            }).to_list(length = None)) #type: ignore
        )
        
    
    async def find_excursions_by_city_id(self, city_id: str):
        return list(
            map(
            self._parse_list,
            await self.excursions_collection.find({"dictionary_data.city": city_id}, {
                "_id": 1,
                "dictionary_data.title": 1#,
                # "dictionary_data.min_age": 1,
                # "dictionary_data.audioguide": 1,
                # "dictionary_data.language": 1,
                # "dictionary_data.form": 1,
                # "dictionary_data.duration_hours": 1,
                # "dictionary_data.price": 1,
                # "dictionary_data.is_can_buy": 1,
                # "dictionary_data.city": 1,
                # "dictionary_data.description": 1,
                # "dictionary_data.program": 1,
                # "dictionary_data.route": 1,

            }).to_list(length = None)) #type: ignore
        )
    
    async def find_hotels_by_city_id(self, city_id: str):
        return list(
            map(
            self._parse_list,
            await self.excursions_collection.find({"dictionary_data.city": city_id}, {
                "_id": 1,
                "dictionary_data.title": 1#,
                # "dictionary_data.": 1,
                # "dictionary_data.": 1,
                # "dictionary_data.": 1,
                # "dictionary_data.": 1,
                # "dictionary_data.": 1,
                # "dictionary_data.": 1,
                # "dictionary_data.": 1,
                # "dictionary_data.": 1,
                # "dictionary_data.": 1,
                # "dictionary_data.description": 1,
            }).to_list(length = None)) #type: ignore
        )
    
    async def find_places_by_city_id(self, city_id: str):
        return list(
            map(
            self._parse_list,
            await self.places_collection.find({"dictionary_data.city": city_id}, {
                "_id": 1,
                "dictionary_data.title": 1
            }.to_list(length = None)) #type^ ignore
            )
        )
    
    async def find_restaurants_by_city_id(self, city_id: str):
        return list(
            map(
            self._parse_list,
            await self.restaurants_collection.find({"dictionary_data.city": city_id}, {
                "_id": 1,
                "dictionary_data.title": 1
            }.to_list(length = None)) #type^ ignore
            )
        )
        
    async def get_city_info_by_city_id(self, city_id: str) -> City:
        events = self.find_events_by_city_id(city_id)
        excursions = self.find_excursions_by_city_id(city_id)
        hotels = self.find_hotels_by_city_id(city_id)
        places = self.find_places_by_city_id(city_id)
        restaurants = self.find_events_by_city_id(city_id)
        city = self.find_city_by_id(city_id)
        return {**city, 
                "events": events, 
                "excursions": excursions,
                "hotels": hotels,
                "places": places,
                "restaurants": restaurants}



CityService = _CityService()
