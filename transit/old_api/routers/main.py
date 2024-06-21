from fastapi import APIRouter


from transit.old_api.routers.transit_gateway.router import router as transit_gateway_router

api_router = APIRouter()
api_router.include_router(transit_gateway_router)
