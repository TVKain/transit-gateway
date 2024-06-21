import json
import re
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import SQLModel

from app.service.vyos.vyos_device import vy_device

router = APIRouter(prefix="/routings", tags=["routings"])


class Routing(SQLModel):
    destination: str
    next_hop: str


@router.get("/")
def get_routings():
    table = vy_device.show(path=["ip", "route", "static"]).result

    return _parse_routings_table(table)


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

    return {"status": "success"}


def _parse_routings_table(table: str):
    routes = []

    route = {}
    # Regular expression pattern to match the routing table entries

    prev_ip = None

    lines = table.strip().split("\n")

    for line in lines[6:]:
        tokens = line.split()

        if len(tokens) == 0:
            continue

        if len(tokens) == 9:
            prev_ip = tokens[1]

            if prev_ip == "0.0.0.0/0":
                continue

            if prev_ip == "169.254.169.254/32":
                continue

            route = {
                "destination": tokens[1],
                "next_hop": tokens[4],
                "interface": tokens[5],
            }

            routes.append(route)

        elif len(tokens) == 7:
            if prev_ip == "0.0.0.0/0":
                continue

            route = {
                "destination": prev_ip,
                "next_hop": tokens[2],
                "interface": tokens[3],
            }

            routes.append(route)

    return routes
