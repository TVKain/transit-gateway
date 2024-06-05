import abc

from transit.drivers.compute.models.compute_driver_build import (
    ComputeDriverBuildInput,
)

from transit.drivers.compute.models.compute_driver_delete import (
    ComputeDriverDeleteInput,
)

from transit.drivers.compute.models.compute_driver_status import (
    ComputeDriverStatusInput,
)


class ComputeDriver(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def build(self, params: ComputeDriverBuildInput) -> str:
        """Build a new vytransit.

        :param name: Optional name for vytransit
        :param amphora_flavor: Optionally specify a flavor
        :param image_tag: tag of the base image for the vytransit instance
        :param network_ids: A list of network IDs to attach to the vytransit

        :raises ComputeBuildException: if compute failed to build VyTransit
        :returns: UUID of amphora
        """

    @abc.abstractmethod
    def delete(self, params: ComputeDriverDeleteInput):
        """Delete a vytransit virtual machine.

        :param compute_id: virtual machine UUID
        """

    @abc.abstractmethod
    def status(self, params: ComputeDriverStatusInput):
        """Retrieve the status of a vytransit virtual machine.

        :param compute_id: virtual machine UUID
        :returns: constant of vytransit status
        """
