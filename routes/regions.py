from fastapi import APIRouter
from routes.cities import handle_cities_exception

from services.city import CityService


router = APIRouter(prefix="/regions", tags=["Regions"])


@router.get("/")
async def list_regions(query: str | None = None):
    with handle_cities_exception():
        return await CityService.list_regions(query)


@router.get("/{region_id}")
async def get_region_data(region_id: str):
    with handle_cities_exception():
        return await CityService.find_region_by_id(region_id)
