from contextlib import contextmanager

from fastapi import APIRouter, HTTPException
from schemas.hotel_data import BaseHotel
from schemas.restaurants import RestaurantRetrieve
from services.city import CityService

router = APIRouter(prefix="/restaurants", tags=["Restaurants Data"])


@contextmanager
def handle_restaurants_exception():
    try:
        yield
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.args[0])


@router.get("/")
async def restaurants_list(query: str | None = None):
    with handle_restaurants_exception():
        return await CityService.list_restaurants()


@router.get("/{restaurant_id}", response_model=RestaurantRetrieve)
async def get_restaurant(restaurant_id: str):
    with handle_restaurants_exception():
        return await CityService.find_restaurant_by_id(restaurant_id)
