# pylint: disable=arguments-differ
from taskflow import task

from oslo_config import cfg

from transit.controller.drivers.compute.drivers.nova_driver import NovaDriver
from transit.controller.drivers.compute.models.compute_driver_build import (
    ComputeDriverBuildInput,
)
from transit.database.repositories.transit_gateway.transit_gateway import (
    TransitGatewayRepository,
)

from transit.database.repositories.transit_gateway.models.transit_gateway_update import (
    TransitGatewayUpdateInput,
)

from transit.common.constants import transit_gateway as transit_constants


class ComputeBuildTask(task.Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.compute_driver = NovaDriver()
        self.transit_gateway_repo = TransitGatewayRepository()

    def execute(self, transit_gateway_id, *args, **kwargs):
        """Create vytransit vm"""
        input_compute_build = ComputeDriverBuildInput(
            name=f"vytransit-{transit_gateway_id}",
            vytransit_flavor_id=cfg.CONF.vytransit.flavor_id,
            vytransit_image_id=cfg.CONF.vytransit.image_id,
            network_ids=[{"uuid": x} for x in cfg.CONF.vytransit.network_ids],
        )

        return self.compute_driver.build(input_compute_build)


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
                    operating_status=transit_constants.ERROR,
                    provisioning_status=transit_constants.ERROR,
                )
            )
        except Exception as e:
            # TODO: update this to log error
            print(e)


class TransitGatewayMarkBootingInDB(task.Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transit_gateway_repo = TransitGatewayRepository()

    def execute(self, transit_gateway_id, *args, **kwargs):
        try:
            self.transit_gateway_repo.update(
                TransitGatewayUpdateInput(
                    id=transit_gateway_id, provisioning_status=transit_constants.BOOTING
                ),
            )
        except Exception as e:
            print(e)

    def revert(self, *args, **kwargs):
        pass


class TransitGatewayMarkReadyInDB(task.Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transit_gateway_repo = TransitGatewayRepository()

    def execute(self, transit_gateway_id, vytransit_id, *args, **kwargs):
        try:
            self.transit_gateway_repo.update(
                TransitGatewayUpdateInput(
                    id=transit_gateway_id,
                    vytransit_id=vytransit_id,
                    provisioning_status=transit_constants.ALLOCATED,
                    operating_status=transit_constants.OPERATIONAL,
                ),
            )
        except Exception as e:
            print(e)

    def revert(self, *args, **kwargs):
        pass
