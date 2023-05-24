from pydantic import BaseModel
from .database import _MongoClient
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection


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
    form: str
    duration_min: str
    ticket_price: str
    is_avaible: bool
    city_id: str
    description: str
    program: str
    route: dict[str, str]


class ExcursionsRetrieve(BaseModel):
    pass


class Hotels(BaseModel):
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


class _CityService(_MongoClient):
    def __init__(self) -> None:
        super().__init__()
        self.cities_collection = self.db["cities"]
        self.regions_collection = self.db["regions"]

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


CityService = _CityService()
