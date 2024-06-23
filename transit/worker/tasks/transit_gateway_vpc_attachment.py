# pylint: disable=arguments-differ
import ipaddress
import os

import logging

from taskflow import task
from taskflow.types import failure


from dotenv import load_dotenv


from transit.database.repositories.transit_gateway_vpc_attachment.models.input import (
    TransitGatewayVPCAttachmentUpdateInput,
)
from transit.database.repositories.transit_gateway_vpc_attachment.transit_gateway_vpc_attachment import (
    TransitGatewayVPCAttachmentRepository,
)


from transit.database.repositories.transit_gateway_vpc_route.transit_gateway_vpc_route import (
    TransitGatewayVPCRouteRepository,
)

from transit.drivers.network.drivers.neutron_driver import NeutronDriver
from transit.drivers.network.models.network_driver_attach_router_to_subnet import (
    NetworkDriverAttachRouterToSubnetInput,
)
from transit.drivers.network.models.network_driver_detach_router_from_subnet import (
    NetworkDriverDetachRouterFromSubnetInput,
)
from transit.drivers.network.models.network_driver_get_subnets import (
    NetworkDriverGetSubnetsInput,
)
from transit.drivers.vytransit.vytransit_driver import VyTransitDriver


load_dotenv()

logger = logging.getLogger(__name__)


class TransitGatewayVPCAttachmentIDToErrorOnRevertTask(task.Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tgw_vpc_att_repo = TransitGatewayVPCAttachmentRepository()

    def execute(self, *args, **kwargs):
        pass

    def revert(self, tgw_vpc_att_id, *args, **kwargs):

        logger.info(f"Reverting TGW VPC Attachment {tgw_vpc_att_id} to ERROR")

        try:
            self.tgw_vpc_att_repo.update(
                TransitGatewayVPCAttachmentUpdateInput(
                    id=tgw_vpc_att_id,
                    status="ERROR",
                )
            )
        except Exception as e:
            print(e)


class TransitGatewayVPCAttachmentAttachRouterToTGWNet(task.Task):
    """
    Attach the VPC router to the TGW subnet
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.network_driver = NeutronDriver()
        self.tgw_vpc_att_repo = TransitGatewayVPCAttachmentRepository()

    def execute(self, tgw_vpc_att_id, vpc_router_id, tgw_vpc_net_id, *args, **kwargs):
        logger.info(
            f"Attaching router {vpc_router_id} to subnet of TGW network {tgw_vpc_net_id}"
        )

        subnet_id = self.network_driver.get_subnets(
            NetworkDriverGetSubnetsInput(network_id=tgw_vpc_net_id)
        )["subnets"][0]["id"]

        result = self.network_driver.attach_router_to_subnet(
            NetworkDriverAttachRouterToSubnetInput(
                router_id=vpc_router_id,
                subnet_id=subnet_id,
            )
        )

        logger.info(f"Router {vpc_router_id} attached to subnet {subnet_id}")

        self.tgw_vpc_att_repo.update(
            TransitGatewayVPCAttachmentUpdateInput(
                id=tgw_vpc_att_id,
                vpc_net_ip=result.ip_address,
                status="READY",
            )
        )

        return dict(
            vpc_router_id=vpc_router_id,
            subnet_id=subnet_id,
            vpc_router_ip=result.ip_address,
        )

    def revert(self, result, *args, **kwargs):
        if isinstance(result, failure.Failure):
            return

        logger.info(
            f"Detaching router {result['vpc_router_id']} from subnet {result['subnet_id']}"
        )

        self.network_driver.detach_router_from_subnet(
            NetworkDriverDetachRouterFromSubnetInput(
                router_id=result["vpc_router_id"], subnet_id=result["subnet_id"]
            )
        )


class TransitGatewayVPCAttachmentDetachRouterFromTGWNet(task.Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.network_driver = NeutronDriver()
        self.tgw_vpc_att_repo = TransitGatewayVPCAttachmentRepository()

    def execute(self, vpc_router_id, tgw_vpc_net_id, *args, **kwargs):
        logger.info(
            f"Detaching router {vpc_router_id} from subnet of TGW network {tgw_vpc_net_id}"
        )

        subnet_id = self.network_driver.get_subnets(
            NetworkDriverGetSubnetsInput(network_id=tgw_vpc_net_id)
        )["subnets"][0]["id"]

        self.network_driver.detach_router_from_subnet(
            NetworkDriverDetachRouterFromSubnetInput(
                router_id=vpc_router_id,
                subnet_id=subnet_id,
            )
        )

        logger.info(f"Router {vpc_router_id} detached from subnet {subnet_id}")

    def revert(self, result, *args, **kwargs):
        if isinstance(result, failure.Failure):
            return


class TransitGatewayVPCAttachmentDeleteAttachmentFromDB(task.Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tgw_vpc_att_repo = TransitGatewayVPCAttachmentRepository()

    def execute(self, tgw_vpc_att_id, *args, **kwargs):
        logger.info(f"Deleting TGW VPC Attachment {tgw_vpc_att_id}")

        self.tgw_vpc_att_repo.delete(tgw_vpc_att_id)

    def revert(self, result, *args, **kwargs):
        if isinstance(result, failure.Failure):
            return


class TransitGatewayVPCAttachmentAddRouteIfPossible(task.Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.network_driver = NeutronDriver()
        self.tgw_vpc_att_repo = TransitGatewayVPCAttachmentRepository()
        self.tgw_vpc_route_repo = TransitGatewayVPCRouteRepository()

    def execute(
        self,
        tgw_vpc_att_id,
        tgw_management_ip,
        vpc_cidr,
        tgw_vpc_net_ip,
        transit_gateway_id,
        vpc_router_info,
        *args,
        **kwargs,
    ):
        logger.info(f"Adding route to VPC CIDR {vpc_cidr} to TGW {transit_gateway_id}")

        vytransit_driver = VyTransitDriver(tgw_management_ip)

        overlap = self._check_cidr_overlap(
            tgw_vpc_att_id=tgw_vpc_att_id,
            vpc_cidr=vpc_cidr,
            transit_gateway_id=transit_gateway_id,
        )

        logger.info(f"Overlap: {overlap}")

        if not overlap:
            vytransit_driver.add_vpc_route(vpc_cidr, vpc_router_info["vpc_router_ip"])

        logger.info(
            f"Updated TGW VPC Attachment {tgw_vpc_att_id} with IP {vpc_router_info['vpc_router_ip']}"
        )

        tgw_vpc_route = self.tgw_vpc_route_repo.create(
            vpc_attachment_id=tgw_vpc_att_id,
            destination_cidr=vpc_cidr,
            status="ACTIVE",
        )

        return dict(
            vpc_cidr=vpc_cidr,
            vpc_router_ip=vpc_router_info["vpc_router_ip"],
            tgw_vpc_net_ip=tgw_vpc_net_ip,
            tgw_management_ip=tgw_management_ip,
            tgw_vpc_route_id=tgw_vpc_route.id,
        )

    def _check_cidr_overlap(self, tgw_vpc_att_id, vpc_cidr, transit_gateway_id):
        vpc_cidr = ipaddress.IPv4Network(vpc_cidr)

        tgw_vpc_atts = self.tgw_vpc_att_repo.get_all(
            transit_gateway_id=transit_gateway_id
        )

        overlap = False
        for tgw_vpc_att in tgw_vpc_atts:
            if tgw_vpc_att.id == tgw_vpc_att_id:
                continue

            tgw_vpc_net_cidr = ipaddress.IPv4Network(tgw_vpc_att.vpc_cidr)
            if vpc_cidr.overlaps(tgw_vpc_net_cidr):
                overlap = True
                break

        return overlap

    def revert(self, result, *args, **kwargs):
        if isinstance(result, failure.Failure):
            return

        logger.info(
            f"Detaching router {result['vpc_router_id']} from subnet {result['subnet_id']}"
        )

        vytransit_driver = VyTransitDriver(result["tgw_management_ip"])
        vytransit_driver.remove_vpc_route(result["vpc_cidr"], result["vpc_router_ip"])

        self.tgw_vpc_route_repo.delete(result["tgw_vpc_route_id"])
