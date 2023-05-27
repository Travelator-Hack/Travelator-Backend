from pydantic import BaseModel

from schemas.city import BaseCity
from schemas.hotel_data import BaseHotel
from .database import _MongoClient
from bson.objectid import ObjectId


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

    async def find_cities_by_region_id(self, region_id: str):
        return list(
            map(
                self._parse_list,
                await self.cities_collection.find({"dictionary_data.region": region_id}).to_list(length=3000),  # type: ignore
            )
        )

    async def find_city_by_id(self, _id: str) -> BaseCity:
        city = await self.cities_collection.find_one({"_id": ObjectId(_id)})
        if not city:
            raise ValueError("City not found")
        return BaseCity.from_dict(city)

    async def list_cities(self):
        """Returns brief information on cities."""
        return list(
            map(
                self._parse_list,
                (await self.cities_collection.find({}, {"dictionary_data.title": 1, "_id": 1}).sort("dictionary_data.sort", -1).to_list(length=None)),  # type: ignore
            )
        )

    async def find_events_by_city_id(self, city_id: str, limit: int | None):
        cursor = self.events_collection.find(
            {"dictionary_data.city": city_id},
            {
                "_id": 1,
                "dictionary_data.title": 1,
            },
        )
        if limit is not None:
            cursor = cursor.limit(limit)
        return list(
            map(
                self._parse_list,
                await cursor.to_list(length=None),  # type: ignore
            )
        )

    async def find_excursions_by_city_id(self, city_id: str, limit: int | None):
        cursor = self.excursions_collection.find(
            {"dictionary_data.city": city_id},
            {
                "_id": 1,
                "dictionary_data.title": 1,
            },
        )
        if limit is not None:
            cursor = cursor.limit(limit)
        return list(
            map(
                self._parse_list,
                await cursor.to_list(length=None),  # type: ignore
            )
        )

    async def find_hotels_by_city_id(self, city_id: str, limit: int | None):
        cursor = self.hotels_collection.find(
            {"dictionary_data.city": city_id},
            {
                "_id": 1,
                "dictionary_data.title": 1,
            },
        )
        if limit is not None:
            cursor = cursor.limit(limit)
        return list(
            map(
                self._parse_list,
                await cursor.to_list(length=None),  # type: ignore
            )
        )

    async def find_places_by_city_id(self, city_id: str, limit: int | None):
        cursor = self.places_collection.find(
            {"dictionary_data.city": city_id},
            {"_id": 1, "dictionary_data.title": 1},
        )
        if limit is not None:
            cursor = cursor.limit(limit)
        return list(
            map(
                self._parse_list,
                await cursor.to_list(
                    length=None,  # type: ignore
                ),
            )
        )

    async def find_restaurants_by_city_id(self, city_id: str):
        return list(
            map(
                self._parse_list,
                await self.restaurants_collection.find(
                    {"dictionary_data.city": city_id},
                    {"_id": 1, "dictionary_data.title": 1},
                ).to_list(
                    length=None  # type: ignore
                ),  
            )
        )
    async def find_hotel_by_id(self, _id: str) -> BaseHotel:
        hotel = await self.hotels_collection.find_one({"_id": ObjectId(_id)})
        if not hotel:
            raise ValueError("City not found")
        return BaseHotel.from_dict(hotel)

    async def list_hotels(self):
        """Returns brief information on hotels."""
        return list(
            map(
                self._parse_list,
                (await self.hotels_collection.find({}).sort("dictionary_data.sort", -1).to_list(length=None)),  # type: ignore
            )
        )


CityService = _CityService()
