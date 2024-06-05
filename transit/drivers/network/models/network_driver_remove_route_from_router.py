from pydantic import BaseModel

from transit.drivers.network.models.network_driver_route import NetworkDriverRoute


class NetworkDriverRemoveRouteFromRouterInput(BaseModel):
    router_id: str
    route: NetworkDriverRoute


class NetworkDriverRemoveRouteFromRouterOutput(BaseModel):
    router_id: str
    routes: list[NetworkDriverRoute]
