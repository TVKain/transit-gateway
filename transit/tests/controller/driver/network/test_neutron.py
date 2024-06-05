import pytest

from transit.tests.fixtures import setup_prepare


from transit.drivers.network.drivers.neutron_driver import NeutronDriver


from transit.drivers.network.models.network_driver_get_subnets import (
    NetworkDriverGetSubnetsInput,
)

from transit.drivers.network.models.network_driver_attach_router_to_subnet import (
    NetworkDriverAttachRouterToSubnetInput,
)

from transit.drivers.network.models.network_driver_detach_router_from_subnet import (
    NetworkDriverDetachRouterFromSubnetInput,
)

from transit.drivers.network.models.network_driver_add_route_to_router import (
    NetworkDriverAddRouteToRouterInput,
    NetworkDriverAddRouteToRouterOutput,
)

from transit.drivers.network.models.network_driver_remove_route_from_router import (
    NetworkDriverRemoveRouteFromRouterInput,
    NetworkDriverRemoveRouteFromRouterOutput,
)


def test_add_route():
    pass


def test_get_subnets():
    neutron_driver = NeutronDriver()

    output = neutron_driver.get_subnets(
        NetworkDriverGetSubnetsInput(network_id="32016ada-3198-4549-b137-f1577589ff76")
    )

    print(output)


def test_get_subnets_fail():
    neutron_driver = NeutronDriver()

    with pytest.raises(Exception):
        neutron_driver.get_subnets(NetworkDriverGetSubnetsInput(network_id="not-exist"))


def test_attach_router_to_subnet():
    neutron_driver = NeutronDriver()

    output = neutron_driver.attach_router_to_subnet(
        NetworkDriverAttachRouterToSubnetInput(
            router_id="59ac5bf2-e3c0-462e-8d95-7ed820f3f0c6",
            subnet_id="b38247bd-cc9f-404e-85ca-ddcf2d5fe02b",
        )
    )

    print(output)


def test_detach_router_from_subnet():
    neutron_driver = NeutronDriver()

    neutron_driver.detach_router_from_subnet(
        NetworkDriverDetachRouterFromSubnetInput(
            router_id="59ac5bf2-e3c0-462e-8d95-7ed820f3f0c6",
            subnet_id="b38247bd-cc9f-404e-85ca-ddcf2d5fe02b",
        )
    )


def test_add_route_to_router():
    neutron_driver = NeutronDriver()

    neutron_driver.add_route_to_router(
        params=NetworkDriverAddRouteToRouterInput(
            router_id="59ac5bf2-e3c0-462e-8d95-7ed820f3f0c6",
            route={"destination": "10.0.0.0/24", "next_hop": "172.0.0.34"},
        )
    )


def test_remove_route_from_router():
    neutron_driver = NeutronDriver()

    neutron_driver.remove_route_from_router(
        params=NetworkDriverAddRouteToRouterInput(
            router_id="59ac5bf2-e3c0-462e-8d95-7ed820f3f0c6",
            route={"destination": "10.0.0.0/24", "next_hop": "172.0.0.34"},
        )
    )
