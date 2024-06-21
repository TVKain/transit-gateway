# pylint: disable=arguments-differ
import ipaddress
import os

import logging

from taskflow import task
from taskflow.types import failure


from dotenv import load_dotenv


from transit.database.repositories.transit_gateway.transit_gateway import (
    TransitGatewayRepository,
)
from transit.database.repositories.transit_gateway_vpc_attachment.transit_gateway_vpc_attachment import (
    TransitGatewayVPCAttachmentRepository,
)
from transit.database.repositories.transit_gateway_vpc_route.transit_gateway_vpc_route import (
    TransitGatewayVPCRouteRepository,
)

from transit.drivers.vytransit.vytransit_driver import VyTransitDriver


load_dotenv()

logger = logging.getLogger(__name__)


class TransitGatewayVPCRouteIDToErrorOnRevertTask(task.Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tgw_vpc_route_repo = TransitGatewayVPCRouteRepository()

    def execute(self, *args, **kwargs):
        pass

    def revert(self, tgw_vpc_route_id, *args, **kwargs):

        logger.info(f"Reverting TGW VPC Route {tgw_vpc_route_id} to ERROR")

        try:
            self.tgw_vpc_route_repo.update(
                ident=tgw_vpc_route_id,
                status="ERROR",
            )
        except Exception as e:
            print(e)


class TransitGatewayVPCRouteDeleteTask(task.Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tgw_vpc_route_repo = TransitGatewayVPCRouteRepository()
        self.tgw_vpc_att_repo = TransitGatewayVPCAttachmentRepository()
        self.tgw_repo = TransitGatewayRepository()

    def execute(
        self,
        destination_cidr,
        tgw_vpc_route_id,
        vpc_net_ip,
        tgw_management_ip,
        *args,
        **kwargs,
    ):
        vytransit_driver = VyTransitDriver(tgw_management_ip)

        vytransit_driver.remove_vpc_route(destination_cidr, vpc_net_ip)

        self.tgw_vpc_route_repo.delete(ident=tgw_vpc_route_id)

    def revert(self, result, *args, **kwargs):
        pass


class TransitGatewayVPCRouteCreateTask(task.Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tgw_vpc_route_repo = TransitGatewayVPCRouteRepository()
        self.tgw_vpc_att_repo = TransitGatewayVPCAttachmentRepository()
        self.tgw_repo = TransitGatewayRepository()

    def execute(
        self,
        tgw_vpc_route_id,
        tgw_vpc_att_id,
        destination_cidr,
        *args,
        **kwargs,
    ):
        tgw_vpc_att = self.tgw_vpc_att_repo.get(ident=tgw_vpc_att_id)

        tgw = self.tgw_repo.get(tgw_vpc_att.transit_gateway_id)

        vytransit_driver = VyTransitDriver(tgw.management_ip)

        vytransit_driver.add_vpc_route(destination_cidr, tgw_vpc_att.vpc_net_ip)

        self.tgw_vpc_route_repo.update(
            ident=tgw_vpc_route_id,
            status="ACTIVE",
        )

        return dict(
            tgw_management_ip=tgw.management_ip,
            vpc_router_ip=tgw_vpc_att.vpc_net_ip,
            destination_cidr=destination_cidr,
        )

    def revert(self, result, *args, **kwargs):
        vytransit_driver = VyTransitDriver(result["tgw_management_ip"])

        vytransit_driver.remove_vpc_route(
            result["destination_cidr"], result["vpc_router_ip"]
        )
