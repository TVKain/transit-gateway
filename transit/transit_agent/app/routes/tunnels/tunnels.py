import logging

import requests

from fastapi import APIRouter
from sqlmodel import SQLModel


from app.service.vyos.vyos_device import vy_device

router = APIRouter(prefix="/tunnels", tags=["tunnels"])


class AddTunnelRequest(SQLModel):

    tunnel_interface_ip: str  # IP address of tunnel interface
    remote_tunnel_interface_ip: str  # IP address of remote tunnel interface

    tun_num: str  # Determine the name of tun interface
    tun_ip: str  # Determine the ip address of tun interface


# TODO: set vpn ipsec options disable-route-autoinstall


class DeleteTunnelRequest(SQLModel):
    tunnel_id: str

    tunnel_interface_ip: str
    remote_tunnel_interface_ip: str

    tun_num: str


"""
example curl 
curl -X POST -F 
    data='{"op": "set", "path": ["interfaces", "dummy", "dum1", "address"], "value": "203.0.113.76/32"}' -F key=qwerty http://192.168.1.1:8080/configure

"""


@router.post("/")
def add_tunnel(request: AddTunnelRequest):

    response = vy_device.configure_set(
        path=[
            ["interfaces", "tunnel", f"tun{request.tun_num}", "encapsulation", "gre"],
            [
                "interfaces",
                "tunnel",
                f"tun{request.tun_num}",
                "address",
                f"{request.tun_ip}",
            ],
            [
                "interfaces",
                "tunnel",
                f"tun{request.tun_num}",
                "source-address",
                f"{request.tunnel_interface_ip}",
            ],
            [
                "interfaces",
                "tunnel",
                f"tun{request.tun_num}",
                "remote",
                f"{request.remote_tunnel_interface_ip}",
            ],
        ]
    )

    print(response)


@router.delete("/{tunnel_id}")
def delete_tunnel(tunnel_id: str):
    response = vy_device.configure_delete(
        path=[
            "interfaces",
            "tunnel",
            f"tun{tunnel_id}",
        ]
    )

    print(response)
