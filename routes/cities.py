from contextlib import contextmanager
from fastapi import APIRouter, HTTPException
from schemas.city import BaseCity

from services.city import CityService


router = APIRouter(prefix="/cities", tags=["Cities Data"])


@contextmanager
def handle_cities_exception():
    try:
        yield
    except Exception as e:
        raise HTTPException(status_code=500, detail=e.args[0])


@router.get("/")
async def cities_list(query: str | None = None):
    with handle_cities_exception():
        return await CityService.list_cities(query)


@router.get("/{city_id}", response_model=BaseCity)
async def get_city(city_id: str):
    with handle_cities_exception():
        return await CityService.find_city_by_id(city_id)


@router.get("/{city_id}/events")
async def get_city_events(city_id: str, limit: int | None = 10):
    with handle_cities_exception():
        return await CityService.find_events_by_city_id(city_id, limit)


@router.get("/{city_id}/excursions")
async def get_city_excursions(city_id: str, limit: int | None = 10):
    with handle_cities_exception():
        return await CityService.find_excursions_by_city_id(city_id, limit)


@router.get("/{city_id}/hotels")
async def get_city_hotels(city_id: str, limit: int | None = 10):
    with handle_cities_exception():
        return await CityService.find_hotels_by_city_id(city_id, limit)


@router.get("/{city_id}/places")
async def get_city_places(city_id: str, limit: int | None = 10):
    with handle_cities_exception():
        return await CityService.find_places_by_city_id(city_id, limit)
