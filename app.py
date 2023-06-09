from fastapi import FastAPI
from routes import auth_router, cities_router, regions_router, hotels_router, restaurants_router, reviews_router, rec_router
from fastapi.middleware.cors import CORSMiddleware

from services.utils import init_indices


app = FastAPI(title="Travelator REST API", version="0.0.1amogus")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "PATCH", "DELETE", "PUT"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(cities_router)
app.include_router(regions_router)
app.include_router(hotels_router)
app.include_router(restaurants_router)
app.include_router(reviews_router)
app.include_router(rec_router)


@app.on_event('startup')
async def init_app():
    await init_indices()
