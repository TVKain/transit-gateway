import abc

from transit.drivers.network.models.network_driver_add_route_to_router import (
    NetworkDriverAddRouteToRouterInput,
    NetworkDriverAddRouteToRouterOutput,
)

from transit.drivers.network.models.network_driver_remove_route_from_router import (
    NetworkDriverRemoveRouteFromRouterInput,
    NetworkDriverRemoveRouteFromRouterOutput,
)

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


class NetworkDriver(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def attach_router_to_subnet(
        self, params: NetworkDriverAttachRouterToSubnetInput
    ) -> NetworkDriverAttachRouterToSubnetOutput:
        """
        Attach router to subnet
        """

    @abc.abstractmethod
    def get_subnets(
        self, params: NetworkDriverGetSubnetsInput
    ) -> NetworkDriverGetSubnetsOutput:
        """_summary_"""

    @abc.abstractmethod
    def detach_router_from_subnet(
        self, params: NetworkDriverDetachRouterFromSubnetInput
    ):
        """
        Detach router from subnet
        """

    @abc.abstractmethod
    def add_route_to_router(
        self, params: NetworkDriverAddRouteToRouterInput
    ) -> NetworkDriverAddRouteToRouterOutput:
        """
        Add route to router
        """

    @abc.abstractmethod
    def remove_route_from_router(
        self, params: NetworkDriverRemoveRouteFromRouterInput
    ) -> NetworkDriverRemoveRouteFromRouterOutput:
        """
        Remove route from router
        """
