from enum import Enum
from pydantic import BaseModel


class TripTarget(str, Enum):
    gastro = 'gastro'
    cultural = 'cultural'
    recreation = 'recreation'


class TransportType(str, Enum):
    aero = 'aero'
    rails = 'rails'
    car = 'car'


class SurveyForm(BaseModel):
    current_city: str
    visited_regions: list[str] | None
    wanted_regions: list[str] | None
    transport_type: list[str] | None
    budget: float | None
    target: list[TripTarget]
