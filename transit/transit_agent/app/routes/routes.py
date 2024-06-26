from fastapi import APIRouter


from app.routes.interfaces.interfaces import router as interfaces_router

from app.routes.routings.routings import router as routings_router

from app.routes.health.health import router as health_router

from app.routes.tunnels.tunnels import router as tunnels_router

api = APIRouter()


api.include_router(interfaces_router)
api.include_router(routings_router)
api.include_router(health_router)
api.include_router(tunnels_router)
