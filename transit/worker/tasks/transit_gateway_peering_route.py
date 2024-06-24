import logging

from taskflow import task

from transit.database.repositories.transit_gateway_peering_route.transit_gateway_peering_route import (
    TransitGatewayPeeringRouteRepository,
)


from transit.drivers.vytransit.vytransit_driver import VyTransitDriver

logger = logging.getLogger(__name__)


class TransitGatewayPeerringRouteIDToErrorOnRevertTask(task.Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tgw_peer_route_repo = TransitGatewayPeeringRouteRepository()

    def execute(self, *args, **kwargs):
        pass

    def revert(self, transit_gateway_peering_route_id, *args, **kwargs):

        logger.info(
            f"Reverting TGW Peering Route {transit_gateway_peering_route_id} to ERROR"
        )

        try:
            self.tgw_peer_route_repo.update(
                ident=transit_gateway_peering_route_id,
                status="ERROR",
            )
        except Exception as e:
            print(e)


class TransitGatewayPeeringRouteCreate(task.Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tgw_peer_route_repo = TransitGatewayPeeringRouteRepository()

    def execute(
        self,
        destination_cidr,
        tgw_management_ip,
        remote_peering_interface_ip,
        *args,
        **kwargs,
    ):
        vytransit_driver = VyTransitDriver(tgw_management_ip)

        try:
            vytransit_driver.add_vpc_route(
                destination_cidr, remote_peering_interface_ip
            )
        except Exception as e:
            raise e from e

    def revert(self, *args, **kwargs):
        pass
