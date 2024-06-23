from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import SQLModel

from app.service.vyos.vyos_device import vy_device

router = APIRouter(prefix="/routings", tags=["routings"])


class Routing(SQLModel):
    destination: str
    next_hop: str


@router.post("/")
def add_routing(routing: Routing):
    vy_device.configure_set(
        path=[
            "protocols",
            "static",
            "route",
            routing.destination,
            "next-hop",
            routing.next_hop,
        ]
    )

    vy_device.config_file_save()

    return {"status": "success"}


@router.delete("/")
def delete_routing(routing: Routing):
    vy_device.configure_delete(
        path=[
            "protocols",
            "static",
            "route",
            routing.destination,
            "next-hop",
            routing.next_hop,
        ]
    )

    vy_device.config_file_save()

    return {"status": "success"}
