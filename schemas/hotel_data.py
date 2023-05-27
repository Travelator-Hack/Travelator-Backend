from dataclasses import dataclass
from typing import Any, Mapping, no_type_check

from pydantic import BaseModel


@dataclass
class Coordinates:
    x: float = 0.0
    y: float = 0.0


class ModelWithID(BaseModel):
    id: str


class HotelPlan(BaseModel):
    name: str
    description: str


class HotelRoom(BaseModel):
    name: str
    description: str
    amenities: list[str]
    rate_plans: list[HotelPlan]


class BaseHotel(ModelWithID):
    pos: Coordinates | Any
    address: str
    description: str
    center_distance: float
    city: str
    stars: str
    title: str
    region: str  
    hotel_rooms: list[dict]

    @classmethod
    @no_type_check
    def from_dict(cls, obj: Mapping):
        unpacked: dict = obj.get("dictionary_data", {})
        return cls(
            id=str(obj.get("_id")),
            pos=Coordinates(
                x=unpacked["geo_data"]["coordinates"][0],
                y=unpacked["geo_data"]["coordinates"][1],
            ),
            center_distance=unpacked.get('geo_data', {}).get('center_distance'),  # type: ignore
            address=unpacked.get("address"),  # type: ignore
            description=unpacked.get('description'),  # type: ignore 
            city=unpacked.get("city"),  # type: ignore
            hotel_rooms=[HotelRoom(**r) for r in unpacked["rooms"]],  # type: ignore
            stars=unpacked.get("stars"),  # type: ignore
            title=unpacked.get("title"),  # type: ignore
            region=unpacked.get("region"),  # type: ignore
        )