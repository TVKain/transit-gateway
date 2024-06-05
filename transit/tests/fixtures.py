import pytest

from transit.common.service import prepare_configuration


@pytest.fixture(scope="session", autouse=True)
def setup_prepare():
    argv_inject = ["", "--config-file", "~/transit-migrate/transit/sample.conf"]
    print("Here")
    prepare_configuration(argv_inject)
