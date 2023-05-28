from datetime import datetime
from enum import Enum
from typing import Mapping

from pydantic import Field, BaseModel
from .base import ModelWithID


class ReviewType(str, Enum):
    hotel = 'hotel'
    restaurant = 'restaurant'
    tour = 'tour'


class ReviewRating(str, Enum):
    bad = 'bad'
    neutral = 'neutral'
    good = 'good'


class ReviewCreation(BaseModel):
    entity_id: str
    rating: ReviewRating
    type: ReviewType
    title: str = Field(max_length=100)
    description: str = Field(max_length=500)


class ReviewRetrieve(ReviewCreation, ModelWithID):
    username: str
    ts_created: datetime

    @classmethod
    def from_dict(cls, obj: Mapping[str, str]):
        return cls(
            id=str(obj.get('_id')),
            entity_id=obj.get('entity_id'),  # type: ignore
            rating=ReviewRating(obj.get('rating')),
            type=ReviewType(obj.get('type')),
            username=obj.get('username'),  # type: ignore
            title=obj.get('title'),  # type: ignore
            description=obj.get('description'),  # type: ignore
            ts_created=obj.get('ts_created'),  # type: ignore
        )
