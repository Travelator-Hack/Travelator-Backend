from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth_router


app = FastAPI(title='Travelator REST API', version='0.0.1amogus')


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "PATCH", "DELETE", "PUT"],
    allow_headers=["*"],
)

app.include_router(auth_router)
