import logging


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

    response = vy_device.configure_set(
        path=[
            f"interfaces vti vti{request.vti_num} address {request.vti_ip}",
        ]
    )

    if response.error:
        return {"status": "error", "message": response.error}

    logging.info(
        f"VTI interface vti{request.vti_num} created with ip address {request.vti_ip}"
    )

    response = vy_device.configure_set(
        path=[
            f"vpn ipsec authentication psk {request.tunnel_id} id {request.tunnel_interface_ip}",
        ]
    )

    if response.error:
        return {"status": "error", "message": response.error}

    response = vy_device.configure_set(
        path=[
            f"vpn ipsec authentication psk {request.tunnel_id} id {request.remote_tunnel_interface_ip}",
        ]
    )

    if response.error:
        return {"status": "error", "message": response.error}

    response = vy_device.configure_set(
        path=[
            f"vpn ipsec authentication psk {request.tunnel_id} secret  {request.secret_key}",
        ]
    )

    if response.error:
        return {"status": "error", "message": response.error}

    logging.info(f"Secret key for tunnel and id {request.tunnel_id} set")

    # set vpn ipsec ike-group tunnel-ike-group
    response = vy_device.configure_set(
        path=[
            f"vpn ipsec site-to-site peer {request.tunnel_id} ike-group tunnel-ike-group",
        ]
    )

    if response.error:
        return {"status": "error", "message": response.error}

    # set vpn ipsec site-to-site peer [tunnel_id] authentication local-id [tunnel_interface_ip]
    response = vy_device.configure_set(
        path=[
            f"vpn ipsec site-to-site peer {request.tunnel_id} authentication local-id {request.tunnel_interface_ip}",
        ]
    )

    if response.error:
        return {"status": "error", "message": response.error}

    # set vpn ipsec site-to-site peer [tunnel_id] authentication remote-id [remote_tunnel_interface_ip]
    response = vy_device.configure_set(
        path=[
            f"vpn ipsec site-to-site peer {request.tunnel_id} authentication remote-id {request.remote_tunnel_interface_ip}",
        ]
    )

    if response.error:
        return {"status": "error", "message": response.error}

    # set vpn ipsec site-to-site peer [tunnel_id] authentication mode 'pre-shared-secret'
    response = vy_device.configure_set(
        path=[
            f"vpn ipsec site-to-site peer {request.tunnel_id} authentication mode pre-shared-secret",
        ]
    )

    if response.error:
        return {"status": "error", "message": response.error}

    # Assumes that the tunnel-ike-group was already created
    # set vpn ipsec site-to-site peer [tunnel_id] ike-group tunnel-ike-group
    response = vy_device.configure_set(
        path=[
            f"vpn ipsec site-to-site peer {request.tunnel_id} ike-group tunnel-ike-group",
        ]
    )

    if response.error:
        return {"status": "error", "message": response.error}

    # set vpn ipsec site-to-site peer [tunnel_id] local-address [tunnel_interface_ip]
    response = vy_device.configure_set(
        path=[
            f"vpn ipsec site-to-site peer {request.tunnel_id} local-address {request.tunnel_interface_ip}",
        ]
    )

    if response.error:
        return {"status": "error", "message": response.error}

    # set vpn ipsec site-to-site peer [tunnel_id] remote-address [remote_address]
    response = vy_device.configure_set(
        path=[
            f"vpn ipsec site-to-site peer {request.tunnel_id} remote-address {request.remote_tunnel_interface_ip}",
        ]
    )

    if response.error:
        return {"status": "error", "message": response.error}

    # set vpn ipsec site-to-site peer [tunnel_id] vti bind vti[vti_num]
    response = vy_device.configure_set(
        path=[
            f"vpn ipsec site-to-site peer {request.tunnel_id} vti bind vti{request.vti_num}",
        ]
    )

    if response.error:
        return {"status": "error", "message": response.error}

    # Assume that the tunnel-esp-group was already created
    response = vy_device.configure_set(
        path=[
            f"vpn ipsec site-to-site peer {request.tunnel_id} vti esp-group tunnel-esp-group",
        ]
    )

    if response.error:
        return {"status": "error", "message": response.error}

    vy_device.config_file_save()

    return {"status": "success"}
