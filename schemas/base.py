from abc import abstractclassmethod

from dataclasses import dataclass
from typing import Mapping
from pydantic import BaseModel


class ModelWithID(BaseModel):
    id: str

    @abstractclassmethod
    def from_dict(cls, obj: Mapping):
        pass



@dataclass
class Coordinates:
    x: float = 0.0
    y: float = 0.0
