# Define route for configure interfaces

import re
from fastapi import APIRouter, Depends, HTTPException

from app.service.vyos.vyos_device import vy_device

router = APIRouter(prefix="/interfaces", tags=["interfaces"])

interface_tag = {
    "eth0": "management",
    "eth1": "transit-vpc",
    "eth2": "transit-peering",
}


@router.get("/")
def get_interfaces():

    return _parse_interfaces_table(vy_device.show(path=["interfaces"]).result)


@router.get("/{interface}")
def get_interface(interface: str):

    interfaces = _parse_interfaces_table(vy_device.show(path=["interfaces"]).result)

    find_interface = [i for i in interfaces if i["name"] == interface]

    if not find_interface:
        raise HTTPException(status_code=404, detail="Interface not found")

    return find_interface[0]


@router.put("/dhpc/{interface}")
def configure_interface_dhcp(interface: str):

    vy_device.configure_set(
        path=["interfaces", "ethernet", interface, "address", "dhcp"]
    )

    return get_interface(interface)


def _parse_interfaces_table(table: str):
    lines = table.strip().split("\n")

    interfaces = []
    interface = {}

    state_map = {
        "u": "up",
        "D": "down",
        "A": "admin down",
    }

    for line in lines[3:]:
        if re.match(r"^\s", line):
            interface["ip_addresses"].append(line.strip())
        else:
            if interface:
                interfaces.append(interface)
            parts = line.split()
            interface = {
                "name": parts[0],
                "ip_addresses": [parts[1]],
                "mac_address": parts[2],
                # "vrf": parts[3], # Don't need this now maybe later
                # "mtu": parts[4],# Don't need this now maybe later
                "state": state_map[parts[5][0]],
                "link": state_map[parts[5][2]],
                "tag": interface_tag.get(parts[0], None),
            }
    if interface:
        interfaces.append(interface)

    return interfaces
