from fastapi import FastAPI
from routes import auth_router, cities_router, regions_router


app = FastAPI(title="Travelator REST API", version="0.0.1amogus")


app.include_router(auth_router)
app.include_router(cities_router)
app.include_router(regions_router)
