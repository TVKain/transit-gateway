from fastapi import APIRouter

from transit.api.routers import transit_gateway


api_router = APIRouter()
api_router.include_router(transit_gateway.router)
