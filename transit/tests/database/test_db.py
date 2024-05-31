# pylint: disable=unused-import
import pytest

from transit.tests.fixtures import setup_prepare

from transit.database.repositories.transit_gateway import TransitGatewayRepository


def test_create_transit():

    transit_repo = TransitGatewayRepository()
    transit_repo.create(
        name="Example Gateway",
        user_id="12345",
        vytransit_id="12345",
        operating_status="active",
        provisioning_status="provisioned",
    )


def test_create_transit_fail():
    transit_repo = TransitGatewayRepository()

    with pytest.raises(Exception):
        transit_repo.create(
            name="Example Gateway",
            user_id="12345",
            vytransit_id="12345",
            operating_status="active",
            provisioning_status="provisioned",
            fail="fail",
        )


def test_update_transit():

    transit_repo = TransitGatewayRepository()

    transit_repo.update(
        ident="38792e43-2d9a-49cd-8054-79e088256686", name="New gateway"
    )


def test_update_transit_fail():
    transit_repo = TransitGatewayRepository()

    with pytest.raises(Exception):
        transit_repo.update(ident="38792e43-2d9a-49cd-8054-79e088256686", sss="fail")
