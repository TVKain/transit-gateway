# Define a route for configuration
# Using fastapi

from app.service.vyos.vyos_device import vy_device

from fastapi import APIRouter

router = APIRouter(prefix="/configuration", tags=["configuration"])


@router.get("/")
def get_configuration():
    return vy_device.retrieve_show_config().result
