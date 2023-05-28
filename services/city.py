from datetime import timedelta
from functools import lru_cache
from asyncache import cached
from cachetools import LRUCache, TTLCache
from pydantic import BaseModel

from schemas.city import BaseCity
from schemas.hotel_data import BaseHotel
from schemas.restaurants import RestaurantRetrieve
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
        self.tours_collection = self.db['tours']
        self.tracks_collection = self.db['tracks']

    def _parse_list(self, data: dict):
        _id = str(data.pop("_id"))
        return {**data["dictionary_data"], "id": _id}

    async def _exists(self, title: str) -> bool:
        return bool(await self.cities_collection.find_one({"title": title}))

    @cached(TTLCache(maxsize=80, ttl=timedelta(hours=1).total_seconds()))
    async def list_regions(self, query: str | None):
        search = {}
        if query is not None:
            search = {"dictionary_data.title": {'$regex': query}}
        return list(
            map(
                self._parse_list,
                await self.regions_collection.find(search, {"dictionary_data.title": 1, "_id": 1}).to_list(length=86),  # type: ignore
            )
        )

    @cached(TTLCache(maxsize=512, ttl=timedelta(hours=1).total_seconds()), key=lambda _, i: i)
    async def find_region_by_id(self, _id: str):
        region = await self.regions_collection.find_one({"_id": ObjectId(_id)})
        if not region:
            raise ValueError("Region not found")
        return self._parse_list(region)  # type: ignore

    @cached(TTLCache(maxsize=512, ttl=timedelta(hours=1).total_seconds()), key=lambda _, i: i)
    async def find_cities_by_region_id(self, region_id: str):
        return list(
            map(
                self._parse_list,
                await self.cities_collection.find({"dictionary_data.region": region_id}).to_list(length=3000),  # type: ignore
            )
        )

    @cached(TTLCache(maxsize=512, ttl=timedelta(hours=1).total_seconds()), key=lambda _, i: i)
    async def find_city_by_id(self, _id: str) -> BaseCity:
        city = await self.cities_collection.find_one({"_id": ObjectId(_id)})
        if not city:
            raise ValueError("City not found")
        print(city)
        region_id = city['dictionary_data'].get('region')
        region = None
        if region_id:
            region = await self.find_region_by_id(city['dictionary_data'].get('region'))
        return BaseCity.from_dict(city, region)

    @cached(TTLCache(maxsize=512, ttl=timedelta(hours=1).total_seconds()))
    async def list_cities(self, query: str | None):
        """Returns brief information on cities."""
        search = {}
        if query is not None:
            search = {"dictionary_data.title": {'$regex': query}}
        return list(
            map(
                self._parse_list,
                (await self.cities_collection.find(search, {"dictionary_data.title": 1, "_id": 1}).sort("dictionary_data.sort", -1).to_list(length=None)),  # type: ignore
            )
        )

    @cached(TTLCache(maxsize=512, ttl=timedelta(hours=1).total_seconds()), key=lambda _, i, l: (i, l))
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

    @cached(TTLCache(maxsize=512, ttl=timedelta(hours=1).total_seconds()), key=lambda _, i, l: (i, l))
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

    @cached(TTLCache(maxsize=512, ttl=timedelta(hours=1).total_seconds()), key=lambda _, i, l: (i, l))
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

    @cached(TTLCache(maxsize=512, ttl=timedelta(hours=1).total_seconds()), key=lambda _, i: i)
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

    @cached(TTLCache(maxsize=512, ttl=timedelta(hours=1).total_seconds()), key=lambda _, i: i)
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

    @cached(TTLCache(maxsize=512, ttl=timedelta(hours=1).total_seconds()), key=lambda _, i: i)
    async def find_hotel_by_id(self, _id: str) -> BaseHotel:
        hotel = await self.hotels_collection.find_one({"_id": ObjectId(_id)})
        if not hotel:
            raise ValueError("City not found")
        return BaseHotel.from_dict(hotel)

    @cached(TTLCache(maxsize=64, ttl=timedelta(hours=1).total_seconds()))
    async def list_hotels(self):
        """Returns brief information on hotels."""
        return list(
            map(
                self._parse_list,
                (await self.hotels_collection.find({}, {"dictionary_data.title": 1, "_id": 1}).to_list(length=None)),  # type: ignore
            )
        )
    
    @cached(TTLCache(maxsize=64, ttl=timedelta(hours=1).total_seconds()))
    async def list_restaurants(self):
        """Returns brief information on restaurants."""
        return list(
            map(
                self._parse_list,
                (await self.restaurants_collection.find({}, {"dictionary_data.title": 1, "_id": 1}).to_list(length=None)),  # type: ignore
            )
        )

    @cached(TTLCache(maxsize=64, ttl=timedelta(hours=1).total_seconds()), key=lambda _, i: i)
    async def find_restaurant_by_id(self, id_: str):
        restaurant = await self.restaurants_collection.find_one({"_id": ObjectId(id_)})
        if not restaurant:
            raise ValueError("Restaurant not found")
        return RestaurantRetrieve.from_dict(restaurant)


CityService = _CityService()
