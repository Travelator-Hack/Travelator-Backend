from dataclasses import dataclass
from typing import Any, Mapping, no_type_check

from pydantic import BaseModel


@dataclass
class Coordinates:
    x: float = 0.0
    y: float = 0.0


class ModelWithID(BaseModel):
    id: str


class BaseHotel(ModelWithID):
    pos: Coordinates | Any
    address: str
    arrival_time: str
    city: str
    departure_time: str
    sort: int
    stars: str
    title: str
    region_id: str  
    hotel_rooms: list[dict]

    @classmethod
    @no_type_check
    def from_dict(cls, obj: Mapping):
        unpacked: dict = obj.get("dictionary_data", {})
        print(unpacked)
        return cls(
            id=str(obj.get("_id")),
            pos=Coordinates(
                x=unpacked["geo_data"]["coordinates"][0],
                y=unpacked["geo_data"]["coordinates"][1],
            ),
            address = unpacked.get("address"),
            arrival_time = unpacked.get("arrival_time"),
            departure_time = unpacked.get("departure_time"),
            city = unpacked.get("city"),
            hotel_rooms=unpacked["hotel_rooms"]["selected"],  # type: ignore
            sort=unpacked.get("sort"),  # type: ignore
            stars=unpacked.get("stars"),  # type: ignore
            title=unpacked.get("title"),  # type: ignore
            region_id=unpacked.get("region"),  # type: ignore
        )