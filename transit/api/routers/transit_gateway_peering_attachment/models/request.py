from sqlmodel import SQLModel


class TransitGatewayPeeringAttachmentCreateRequest(SQLModel):
    name: str | None = None
    transit_gateway_id: str

    remote_tunnel_interface_ip: str
    remote_transit_gateway_id: str

    remote_region_id: str | None = None

    tun_ip: str
    remote_tun_ip: str
    tun_cidr: str
