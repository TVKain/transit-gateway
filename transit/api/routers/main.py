from fastapi import APIRouter


from transit.api.routers.transit_gateway import router

api_router = APIRouter()
api_router.include_router(router.router)
