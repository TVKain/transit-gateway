import openstack.exceptions


from transit.drivers.compute.compute_driver import ComputeDriver
from transit.drivers.compute.exceptions import (
    ComputeBuildException,
    ComputeDeleteException,
    ComputeStatusException,
)
from transit.drivers.compute.models.compute_driver_build import (
    ComputeDriverBuildInput,
)

from transit.drivers.compute.models.compute_driver_delete import (
    ComputeDriverDeleteInput,
)

from transit.drivers.compute.models.compute_driver_status import (
    ComputeDriverStatusInput,
)

from transit.common.client import OpenStackAuth

from transit.common.constants import vytransit


class NovaDriver(ComputeDriver):
    def __init__(self):
        super().__init__()

        self._os_connection = OpenStackAuth.get_connection()

    def build(self, params: ComputeDriverBuildInput) -> str:
        try:
            server = self._os_connection.compute.create_server(
                name=params.name,
                image_id=params.vytransit_image_id,
                flavor_id=params.vytransit_flavor_id,
                networks=params.network_ids,
            )
        except Exception as e:
            raise ComputeBuildException(f"Build vm {params} failed") from e

        server = self._os_connection.compute.wait_for_server(server)

        return server.id

    def delete(self, params: ComputeDriverDeleteInput):
        try:
            self._os_connection.compute.delete_server(
                params.compute_id, ignore_missing=False
            )
        except openstack.exceptions.ResourceNotFound as e:
            raise ComputeDeleteException(
                f"Delete vm fail: No vm with id=f{params.compute_id}"
            ) from e
        except Exception as e:
            raise ComputeDeleteException("Delete vm fail") from e

    def status(self, params: ComputeDriverStatusInput):
        try:
            server = self._os_connection.compute.get_server(params.compute_id)
        except openstack.exceptions.ResourceNotFound as e:
            raise ComputeStatusException(
                f"Get status vm fail: No vm with id=f{params.compute_id}"
            ) from e
        except Exception as e:
            raise ComputeStatusException("Get status vm fail") from e

        return vytransit.UP if server.status == "ACTIVE" else vytransit.DOWN
