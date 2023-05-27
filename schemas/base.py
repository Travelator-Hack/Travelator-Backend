from dataclasses import dataclass
from pydantic import BaseModel


class ModelWithID(BaseModel):
    id: str


@dataclass
class Coordinates:
    x: float = 0.0
    y: float = 0.0
