import pytest

from transit.tests.fixtures import setup_prepare

from transit.common.constants import vytransit
from transit.drivers.compute.drivers.nova_driver import NovaDriver
from transit.drivers.compute.models.compute_driver_build import (
    ComputeDriverBuildInput,
)

from transit.drivers.compute.models.compute_driver_delete import (
    ComputeDriverDeleteInput,
)

from transit.drivers.compute.models.compute_driver_status import (
    ComputeDriverStatusInput,
)


def test_nova_build():
    driver = NovaDriver()

    vytransit_info = ComputeDriverBuildInput(
        name="cirros-test",
        vytransit_image_id="6ff09bc2-3afc-40b5-9929-b2a544617e1a",
        vytransit_flavor_id="0",
        network_ids=[{"uuid": "f8f129ce-bede-4575-ae71-00ea38a193ce"}],
    )

    driver.build(vytransit_info)


def test_nova_delete():
    driver = NovaDriver()

    vm_info = ComputeDriverDeleteInput(
        compute_id="a022509d-766d-4c52-9ae2-b11a2b5d83a8"
    )

    driver.delete(vm_info)


def test_nova_delete_raise():
    driver = NovaDriver()

    vm_info = ComputeDriverStatusInput(compute_id="123")

    with pytest.raises(Exception):
        driver.delete(vm_info)


def test_nova_status():
    driver = NovaDriver()

    vm_info = ComputeDriverStatusInput(
        compute_id="e3416d56-581f-477c-8b36-cf31b68aab8f"
    )

    status = driver.status(vm_info)
    assert status == vytransit.UP
