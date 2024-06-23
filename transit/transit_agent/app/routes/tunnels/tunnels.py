from fastapi import APIRouter
from sqlmodel import SQLModel

from app.service.vyos.vyos_device import vy_device

router = APIRouter(prefix="/tunnels", tags=["tunnels"])


class AddTunnelRequest(SQLModel):
    tunnel_id: str  # Map to  will be tgw peering id
    secret_key: str  # Sent from TGW

    tunnel_interface_ip: str  # IP address of tunnel interface
    remote_tunnel_interface_ip: str  # IP address of remote tunnel interface

    vti_num: str  # Determine the name of vti interface
    vti_ip: str  # Determine the ip address of vti interface


# TODO: set vpn ipsec options disable-route-autoinstall


class DeleteTunnelRequest(SQLModel):
    tunnel_id: str
    secret_key: str

    tunnel_interface_ip: str
    remote_tunnel_interface_ip: str

    vti_num: str


@router.delete("/{tunnel_id}")
def delete_tunnel(tunnel_id: str, request: DeleteTunnelRequest):
    pass


@router.post("/")
def add_tunnel(request: AddTunnelRequest):

    # set vpn ipsec authentication psk [tunnel_id] id [tunnel_interface_ip]
    vy_device.configure_set(
        path=[
            "vpn",
            "ipsec",
            "authentication",
            "psk",
            request.tunnel_id,
            "id",
            request.tunnel_interface_ip,
        ]
    )
    # set vpn ipsec authentication psk [tunnel_id] id [remote_tunnel_interface_ip]
    vy_device.configure_set(
        path=[
            "vpn",
            "ipsec",
            "authentication",
            "psk",
            request.tunnel_id,
            "id",
            request.remote_tunnel_interface_ip,
        ]
    )

    # set vpn ipsec ike-group tunnel-ike-group
    vy_device.configure_set(
        path=[
            "vpn",
            "ipsec",
            "site-to-site",
            "peer",
            request.tunnel_id,
            "authentication",
            "mode",
            "pre-shared-secret",
        ]
    )

    # set vpn ipsec site-to-site peer [tunnel_id] authentication local-id [tunnel_interface_ip]
    vy_device.configure_set(
        path=[
            "vpn",
            "ipsec",
            "site-to-site",
            "peer",
            request.tunnel_id,
            "authentication",
            "local-id",
            request.tunnel_interface_ip,
        ]
    )

    # set vpn ipsec site-to-site peer [tunnel_id] authentication remote-id [remote_tunnel_interface_ip]
    vy_device.configure_set(
        path=[
            "vpn",
            "ipsec",
            "site-to-site",
            "peer",
            request.tunnel_id,
            "authentication",
            "remote-id",
            request.remote_tunnel_interface_ip,
        ]
    )

    # set vpn ipsec site-to-site peer [tunnel_id] authentication mode 'pre-shared-secret'
    vy_device.configure_set(
        path=[
            "vpn",
            "ipsec",
            "site-to-site",
            "peer",
            request.tunnel_id,
            "authentication",
            "mode",
            "pre-shared-secret",
        ]
    )

    # Assumes that the tunnel-ike-group was already created
    # set vpn ipsec site-to-site peer [tunnel_id] ike-group tunnel-ike-group
    vy_device.configure_set(
        path=[
            "vpn",
            "ipsec",
            "site-to-site",
            "peer",
            request.tunnel_id,
            "ike-group",
            "tunnel-ike-group",
        ]
    )

    # set vpn ipsec site-to-site peer [tunnel_id] local-address [tunnel_interface_ip]
    vy_device.configure_set(
        path=[
            "vpn",
            "ipsec",
            "site-to-site",
            "peer",
            request.tunnel_id,
            "local-address",
            request.local_address,
        ]
    )

    # set vpn ipsec site-to-site peer [tunnel_id] remote-address [remote_address]
    vy_device.configure_set(
        path=[
            "vpn",
            "ipsec",
            "site-to-site",
            "peer",
            request.tunnel_id,
            "remote-address",
            request.remote_address,
        ]
    )

    # set interfaces vti vti[vti_num] address [vti_ip]
    vy_device.configure_set(
        path=[
            "interfaces",
            "vti",
            f"vti{request.vti_num}",
            "address",
            request.vti_ip,
        ]
    )

    # set vpn ipsec site-to-site peer [tunnel_id] vti bind vti[vti_num]
    vy_device.configure_set(
        path=[
            "vpn",
            "ipsec",
            "site-to-site",
            "peer",
            f"{request.tunnel_id}",
            "vti",
            "bind",
            f"vti{request.vti_num}",
        ]
    )

    # Assume that the tunnel-esp-group was already created
    vy_device.configure_set(
        path=[
            "vpn",
            "ipsec",
            "site-to-site",
            "peer",
            f"{request.tunnel_id}",
            "esp-group",
            "tunnel-esp-group",
        ]
    )

    vy_device.config_file_save()

    return {"status": "success"}
