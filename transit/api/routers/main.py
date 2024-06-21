from fastapi import APIRouter


from transit.api.routers.transit_gateway.transit_gateway import (
    router as transit_gateway_router,
)

from transit.api.routers.transit_gateway_vpc_attachment.transit_gateway_vpc_attachment import (
    router as transit_gateway_vpc_attachment_router,
)

from transit.api.routers.transit_gateway_vpc_route.transit_gateway_vpc_route import (
    router as transit_gateway_vpc_routes_router,
)

from transit.api.routers.vpc_transit_gateway_route.vpc_transit_gateway_route import (
    router as vpc_transit_gateway_routes_router,
)


api_router = APIRouter()
api_router.include_router(transit_gateway_router)
api_router.include_router(transit_gateway_vpc_attachment_router)
api_router.include_router(transit_gateway_vpc_routes_router)
api_router.include_router(vpc_transit_gateway_routes_router)
