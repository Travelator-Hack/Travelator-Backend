from typing import Any, Mapping

from .base import Coordinates, ModelWithID


class RestaurantRetrieve(ModelWithID):
    title: str
    description: str
    address: str
    region: str
    city: str
    average_bill: float
    recommendation: bool | Any
    pos: Coordinates | Any

    @classmethod
    def from_dict(cls, obj: Mapping, /):
        unpacked: dict[str, Any] = obj.get("dictionary_data", {})
        return cls(
            id=str(obj.get("_id")),
            title=unpacked.get('title'),  # type: ignore
            description=unpacked.get('description'),  # type: ignore
            address=unpacked.get('address'),  # type: ignore
            region=unpacked.get('region'),  # type: ignore
            city=unpacked.get('city')[-1],  # type: ignore
            average_bill=unpacked.get('bill'),  # type: ignore
            recommendation=unpacked.get('russpass_recommendation', False),
            pos=Coordinates(
                x=unpacked["geo_data"]["coordinates"][0],
                y=unpacked["geo_data"]["coordinates"][1],
            ),
        )
