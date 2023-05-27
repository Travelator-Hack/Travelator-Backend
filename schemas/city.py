from typing import Mapping, no_type_check, Any
from pydantic import BaseModel
from dataclasses import dataclass

from .base import Coordinates, ModelWithID



class BaseCity(ModelWithID):
    pos: Coordinates | Any
    travel_line_id: str
    aliases: list[str]
    sort: int
    rating: int
    title: str
    region_id: str

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
            travel_line_id=unpacked.get("travel_line_id"),  # type: ignore
            aliases=unpacked.get("aliases"),  # type: ignore
            sort=unpacked.get("sort"),  # type: ignore
            rating=unpacked.get("rating"),  # type: ignore
            title=unpacked.get("title"),  # type: ignore
            region_id=unpacked.get("region"),  # type: ignore
        )
