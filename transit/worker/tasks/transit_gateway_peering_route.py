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

    def revert(self, tgw_peering_route_id, *args, **kwargs):

        logger.info(f"Reverting TGW Peering Route {tgw_peering_route_id} to ERROR")

        try:
            self.tgw_peer_route_repo.update(
                ident=tgw_peering_route_id,
                status="ERROR",
            )
        except Exception as e:
            print(e)


class TransitGatewayPeeringRouteCreateTask(task.Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tgw_peer_route_repo = TransitGatewayPeeringRouteRepository()

    def execute(
        self,
        destination_cidr,
        tgw_management_ip,
        remote_peering_interface_ip,
        tgw_peering_route_id,
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

        self.tgw_peer_route_repo.update(ident=tgw_peering_route_id, status="ACTIVE")

    def revert(self, *args, **kwargs):
        pass


class TransitGatewayPeeringRouteDeleteTask(task.Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tgw_peer_route_repo = TransitGatewayPeeringRouteRepository()

    def execute(
        self,
        tgw_peering_route_id,
        tgw_management_ip,
        remote_peering_interface_ip,
        *args,
        **kwargs,
    ):
        tgw_peer_route = self.tgw_peer_route_repo.get(tgw_peering_route_id)

        vytransit_driver = VyTransitDriver(tgw_management_ip)

        print(tgw_peer_route.destination_cidr)
        print(remote_peering_interface_ip)

        try:
            vytransit_driver.remove_vpc_route(
                tgw_peer_route.destination_cidr, remote_peering_interface_ip
            )
        except Exception as e:
            raise e from e

        self.tgw_peer_route_repo.delete(tgw_peering_route_id)

    def revert(self, *args, **kwargs):
        pass
