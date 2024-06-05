from transit.common.client import OpenStackAuth

from transit.drivers.network.models.network_driver_get_subnets import (
    NetworkDriverGetSubnetsInput,
    NetworkDriverGetSubnetsOutput,
)

from transit.drivers.network.models.network_driver_attach_router_to_subnet import (
    NetworkDriverAttachRouterToSubnetInput,
    NetworkDriverAttachRouterToSubnetOutput,
)

from transit.drivers.network.models.network_driver_detach_router_from_subnet import (
    NetworkDriverDetachRouterFromSubnetInput,
)

from transit.drivers.network.models.network_driver_add_route_to_router import (
    NetworkDriverAddRouteToRouterInput,
    NetworkDriverAddRouteToRouterOutput,
)


from transit.drivers.network.models.network_driver_remove_route_from_router import (
    NetworkDriverRemoveRouteFromRouterInput,
    NetworkDriverRemoveRouteFromRouterOutput,
)


from transit.drivers.network.network_driver import NetworkDriver

from transit.drivers.network.exceptions import (
    NetworkNotFoundException,
    AttachRouterToSubnetException,
    DetachRouterToSubnetException,
    AddRouteToRouterException,
    RemoveRouteFromRouterException,
)


class NeutronDriver(NetworkDriver):
    def __init__(self):
        super().__init__()

        self._os_connection = OpenStackAuth.get_connection()

    def attach_router_to_subnet(
        self, params: NetworkDriverAttachRouterToSubnetInput
    ) -> NetworkDriverAttachRouterToSubnetOutput:
        try:
            self._os_connection.get_router(params.router_id)
        except Exception as e:
            raise AttachRouterToSubnetException(
                f"Router with id={params.router_id} not found"
            ) from e

        try:
            subnet = self._os_connection.get_subnet_by_id(params.subnet_id)
        except Exception as e:
            raise AttachRouterToSubnetException(
                f"Subnet with id={params.subnet_id} not found"
            ) from e

        try:
            port = self._os_connection.create_port(
                network_id=subnet.network_id, fixed_ips=[{"subnet_id": subnet.id}]
            )

            self._os_connection.add_router_interface(params.router_id, port_id=port.id)

            print(port)
        except Exception as e:
            raise AttachRouterToSubnetException(repr(e)) from e

        return NetworkDriverAttachRouterToSubnetOutput(
            router_id=params.router_id,
            subnet_id=params.subnet_id,
            ip_address=port.fixed_ips[0]["ip_address"],
        )

    def detach_router_from_subnet(
        self, params: NetworkDriverDetachRouterFromSubnetInput
    ):
        try:
            self._os_connection.get_router(params.router_id)
        except Exception as e:
            raise DetachRouterToSubnetException(
                f"Router with id={params.router_id} not found"
            ) from e

        try:
            self._os_connection.get_subnet_by_id(params.subnet_id)
        except Exception as e:
            raise DetachRouterToSubnetException(
                f"Subnet with id={params.subnet_id} not found"
            ) from e

        try:
            self._os_connection.remove_router_interface(
                router=params.router_id, subnet_id=params.subnet_id
            )
        except Exception as e:
            raise DetachRouterToSubnetException(repr(e)) from e

    def add_route_to_router(
        self, params: NetworkDriverAddRouteToRouterInput
    ) -> NetworkDriverAddRouteToRouterOutput:

        try:

            router = self._os_connection.get_router(params.router_id)

            router.routes.append(
                {
                    "destination": params.route.destination,
                    "nexthop": params.route.next_hop,
                }
            )

            new_routes = router.routes

            router = self._os_connection.update_router(
                name_or_id=router.id, routes=new_routes
            )

            print(router)

        except Exception as e:

            raise AddRouteToRouterException(str(e)) from e

    def remove_route_from_router(
        self, params: NetworkDriverRemoveRouteFromRouterInput
    ) -> NetworkDriverRemoveRouteFromRouterOutput:
        """
        Remove route from router
        """

        try:

            router = self._os_connection.get_router(params.router_id)

            router.routes.remove(
                {
                    "destination": params.route.destination,
                    "nexthop": params.route.next_hop,
                }
            )

            new_routes = router.routes

            router = self._os_connection.update_router(
                name_or_id=router.id, routes=new_routes
            )

            print(router)
        except ValueError as e:
            raise RemoveRouteFromRouterException(
                f'No route with destination="{params.route.destination}" and nexthop="{params.route.next_hop}" in routing table'
            ) from e
        except Exception as e:

            raise RemoveRouteFromRouterException(str(e)) from e

    def get_subnets(
        self, params: NetworkDriverGetSubnetsInput
    ) -> NetworkDriverGetSubnetsOutput:

        try:
            self._os_connection.get_network_by_id(id=params.network_id)
        except Exception as e:
            raise NetworkNotFoundException from e

        subnet_generator = self._os_connection.network.subnets(
            network_id=params.network_id
        )

        return {
            "subnets": [
                {
                    "id": subnet.id,
                    "address": subnet.cidr,
                    "network_id": subnet.network_id,
                }
                for subnet in subnet_generator
            ]
        }
