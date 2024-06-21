import logging

from taskflow import task

from transit.database.repositories.vpc_transit_gateway_route.vpc_transit_gateway_route import (
    VPCTransitGatewayRouteRepository,
)
from transit.drivers.network.drivers.neutron_driver import NeutronDriver
from transit.drivers.network.models.network_driver_add_route_to_router import (
    NetworkDriverAddRouteToRouterInput,
)
from transit.drivers.network.models.network_driver_remove_route_from_router import (
    NetworkDriverRemoveRouteFromRouterInput,
)
from transit.drivers.network.models.network_driver_route import NetworkDriverRoute

logger = logging.getLogger(__name__)


class VPCTransitGatewayRouteIDToErrorOnRevertTask(task.Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vpc_tgw_route_repo = VPCTransitGatewayRouteRepository()

    def execute(self, *args, **kwargs):
        pass

    def revert(self, vpc_twg_route_id, *args, **kwargs):

        logger.info(f"Reverting VPC TGW Route {vpc_twg_route_id} to ERROR")

        try:
            self.vpc_tgw_route_repo.update_status(
                ident=vpc_twg_route_id,
                status="ERROR",
            )
        except Exception as e:
            print(e)


class VPCTransitGatewayRouteDeleteTask(task.Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vpc_tgw_route_repo = VPCTransitGatewayRouteRepository()
        self.network_driver = NeutronDriver()

    def execute(
        self,
        vpc_tgw_route_id,
        vpc_router_id,
        destination_cidr,
        tgw_vpc_net_ip,
        *args,
        **kwargs,
    ):
        try:
            self.network_driver.remove_route_from_router(
                NetworkDriverRemoveRouteFromRouterInput(
                    router_id=vpc_router_id,
                    route=NetworkDriverRoute(
                        destination=destination_cidr, next_hop=tgw_vpc_net_ip
                    ),
                )
            )
        except Exception as e:
            logger.error(f"Error deleting route from router: {e}")
            raise e

        self.vpc_tgw_route_repo.delete(
            ident=vpc_tgw_route_id,
        )

        return vpc_tgw_route_id


class VPCTransitGatewayRouteCreateTask(task.Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vpc_tgw_route_repo = VPCTransitGatewayRouteRepository()
        self.network_driver = NeutronDriver()

    def execute(
        self,
        vpc_tgw_route_id,
        vpc_router_id,
        destination_cidr,
        tgw_vpc_net_ip,
        *args,
        **kwargs,
    ):
        try:
            self.network_driver.add_route_to_router(
                NetworkDriverAddRouteToRouterInput(
                    router_id=vpc_router_id,
                    route=NetworkDriverRoute(
                        destination=destination_cidr, next_hop=tgw_vpc_net_ip
                    ),
                )
            )
        except Exception as e:
            logger.error(f"Error adding route to router: {e}")
            raise e

        self.vpc_tgw_route_repo.delete(vpc_tgw_route_id)
        return vpc_tgw_route_id
