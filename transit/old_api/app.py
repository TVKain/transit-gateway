from fastapi import FastAPI

from transit.old_api.routers.main import api_router

app = FastAPI()

app.include_router(api_router)