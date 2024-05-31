import pytest

from transit.common.service import prepare_service


@pytest.fixture(scope="session", autouse=True)
def setup_prepare():
    argv_inject = ["", "--config-file", "~/transit-migrate/transit/sample.conf"]
    prepare_service(argv_inject)
