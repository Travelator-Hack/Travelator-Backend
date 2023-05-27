from contextlib import contextmanager

from fastapi import APIRouter, HTTPException
from schemas.hotel_data import BaseHotel
from services.city import CityService

router = APIRouter(prefix="/hotels", tags=["Hotels Data"])


@contextmanager
def handle_hotels_exception():
    try:
        yield
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.args[0])


@router.get("/")
async def hotels_list(query: str | None = None):
    with handle_hotels_exception():
        return await CityService.list_hotels()


@router.get("/{hotel_id}", response_model=BaseHotel)
async def get_hotel(hotel_id: str):
    with handle_hotels_exception():
        return await CityService.find_hotel_by_id(hotel_id)
