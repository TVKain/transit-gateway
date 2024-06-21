# pylint: disable=arguments-differ
import os

import logging

from taskflow import task
from taskflow.types import failure


from dotenv import load_dotenv

from transit.database.repositories.transit_gateway.models.input import (
    TransitGatewayUpdateInput,
)
from transit.drivers.compute.drivers.nova_driver import NovaDriver
from transit.drivers.compute.models.compute_driver_build import (
    ComputeDriverBuildInput,
)
from transit.database.repositories.transit_gateway.transit_gateway import (
    TransitGatewayRepository,
)
from transit.drivers.compute.models.compute_driver_delete import (
    ComputeDriverDeleteInput,
)
from transit.drivers.network.drivers.neutron_driver import NeutronDriver
from transit.drivers.vytransit.vytransit_driver import VyTransitDriver


load_dotenv()

logger = logging.getLogger(__name__)


class TransitGatewayIDToErrorOnRevertTask(task.Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transit_gateway_repo = TransitGatewayRepository()

    def execute(self, *args, **kwargs):
        pass

    def revert(self, transit_gateway_id, *args, **kwargs):
        """When error this task will be reverted to"""
        try:
            self.transit_gateway_repo.update(
                TransitGatewayUpdateInput(
                    id=transit_gateway_id,
                    status="ERROR",
                )
            )
        except Exception as e:
            print(e)


class TransitGatewayCreateNetwork(task.Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.compute_driver = NovaDriver()
        self.transit_gateway_repo = TransitGatewayRepository()
        self.network_driver = NeutronDriver()

    def execute(self, transit_gateway_id, *args, **kwargs):
        network_id = self.network_driver.create_network(
            name=f"net-vpc-transit-{transit_gateway_id}"
        )

        return network_id

    def revert(self, result, *args, **kwargs):

        if isinstance(result, failure.Failure):
            return

        logger.info(f"Deleting network {result}")

        self.network_driver.delete_network(result)


class TransitGatewayComputeBuildTask(task.Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.compute_driver = NovaDriver()
        self.transit_gateway_repo = TransitGatewayRepository()

    def execute(self, transit_gateway_id, vpc_network_id, *args, **kwargs):
        """Create vytransit vm"""

        network_ids = [
            os.getenv("MANAGEMENT_NETWORK_ID"),
            vpc_network_id,
            os.getenv("PEERING_NETWORK_ID"),
        ]

        input_compute_build = ComputeDriverBuildInput(
            name=f"vytransit-{transit_gateway_id}",
            vytransit_flavor_id=os.getenv("VYTRANSIT_FLAVOR_ID"),
            vytransit_image_id=os.getenv("VYTRANSIT_IMAGE_ID"),
            network_ids=[{"uuid": x} for x in network_ids],
        )

        compute = self.compute_driver.build(input_compute_build)

        logger.info(f"Compute created {compute}")

        management_ip = compute.addresses["net-transit-management"][0]["addr"]
        vpc_network_ip = compute.addresses[f"net-vpc-transit-{transit_gateway_id}"][0][
            "addr"
        ]
        peering_ip = compute.addresses["net-provider"][0]["addr"]

        logger.info(f"Management IP: {management_ip}")
        logger.info(f"VPC Network IP: {vpc_network_ip}")
        logger.info(f"Peering IP: {peering_ip}")

        vy_transit_driver = VyTransitDriver(management_ip=management_ip)

        res = vy_transit_driver.health_check()

        if not res:
            self.compute_driver.delete(ComputeDriverDeleteInput(compute_id=compute.id))
            raise Exception("Vytransit health check failed")

        logger.info("Vytransit health check passed")

        self.transit_gateway_repo.update(
            TransitGatewayUpdateInput(
                id=transit_gateway_id,
                compute_id=compute.id,
                management_ip=management_ip,
                vpc_net_id=vpc_network_id,
                vpc_net_ip=vpc_network_ip,
                peering_net_ip=peering_ip,
            )
        )

        return compute.id

    def revert(self, result, *args, **kwargs):
        pass


class TransitGatewayMarkActiveInDB(task.Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transit_gateway_repo = TransitGatewayRepository()

    def execute(self, transit_gateway_id, vytransit_id, *args, **kwargs):

        self.transit_gateway_repo.update(
            TransitGatewayUpdateInput(
                id=transit_gateway_id,
                compute_id=vytransit_id,
                status="ACTIVE",
            ),
        )

    def revert(self, *args, **kwargs):
        pass
