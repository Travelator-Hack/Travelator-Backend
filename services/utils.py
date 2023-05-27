from services import UserService
from services.city import CityService


async def init_indices():
    """Create or update MongoDB Indices to speedup lookup."""
    # Cities indices
    await CityService.cities_collection.create_index('dictionary_data.region')
    await CityService.cities_collection.create_index('dictionary_data.title')

    # Regions indices
    await CityService.regions_collection.create_index('dictionary_data.title')

    # Events indices
    await CityService.events_collection.create_index('dictionary_data.city')
    await CityService.events_collection.create_index('dictionary_data.region')
    await CityService.events_collection.create_index('dictionary_data.place')

    # Excursions indices
    await CityService.excursions_collection.create_index('dictionary_data.title')
    await CityService.excursions_collection.create_index('dictionary_data.region')
    await CityService.excursions_collection.create_index('dictionary_data.city')

    # Hotels indices
    await CityService.hotels_collection.create_index('dictionary_data.title')
    await CityService.hotels_collection.create_index('dictionary_data.stars')
    await CityService.hotels_collection.create_index('dictionary_data.region')
    await CityService.hotels_collection.create_index('dictionary_data.city')

    # Places indices
    await CityService.hotels_collection.create_index('dictionary_data.title')
    await CityService.hotels_collection.create_index('dictionary_data.city')
    await CityService.hotels_collection.create_index('dictionary_data.region')

    # Restaurants indices
    await CityService.restaurants_collection.create_index('dictionary_data.title')
    await CityService.restaurants_collection.create_index('dictionary_data.region')
    await CityService.restaurants_collection.create_index('dictionary_data.city')

    # Tours indices
    await CityService.tours_collection.create_index('dictionary_data.city')

    # Tracks indices
    await CityService.tracks_collection.create_index('dictionary_data.city')
    await CityService.tracks_collection.create_index('dictionary_data.region')

    # Users indices
    await UserService.users_collection.create_index([('username', 1), ('hashed_password', 1)])
