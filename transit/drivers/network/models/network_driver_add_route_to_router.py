from pydantic import BaseModel

from transit.drivers.network.models.network_driver_route import NetworkDriverRoute


class NetworkDriverAddRouteToRouterInput(BaseModel):
    router_id: str
    route: NetworkDriverRoute


class NetworkDriverAddRouteToRouterOutput(BaseModel):
    router_id: str
    routes: list[NetworkDriverRoute]
