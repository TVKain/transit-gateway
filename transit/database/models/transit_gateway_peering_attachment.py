import uuid

from typing import Optional
from sqlmodel import SQLModel, Field

from pydantic import ConfigDict


# Maximum of 4 Transit Gateway Peering Attachments per Transit Gateway
class TransitGatewayPeeringAttachmentModel(SQLModel, table=True):
    __tablename__ = "transit_gateway_peering_attachments"
    model_config = ConfigDict(extra="ignore")

    id: Optional[str] = Field(
        default_factory=lambda: f"tgw-peer-att-{uuid.uuid4()}", primary_key=True
    )

    # Transit gateway for this peering attachment to be attached to
    transit_gateway_id: Optional[str] = Field(foreign_key="transit_gateways.id")

    # ID of the remote transit gateway to peer with
    remote_transit_gateway_id: Optional[str] = None

    # Status of the peering attachment
    status: Optional[str] = None

    # The IP address of the interface used to tunnel
    tunnel_interface_ip: Optional[str] = None

    # The IP address of the remote interface used to tunnel for the remote transit gateway
    remote_tunnel_interface_ip: Optional[str] = None

    # Virtual Tunnel Interface Number - this is will be used in the name of vti e.g vti-{vti_num}
    tun_num: Optional[int] = None  # Virtual Tunnel Interface Number

    # Virtual Tunnel Interface IP
    tun_ip: Optional[str] = None  # Virtual Tunnel Interface IP
    remote_tun_ip: Optional[str] = None  # Remote Virtual Tunnel Interface IP
    tun_cidr: Optional[str] = (
        None  # Virtual Tunnel Interface CIDR must be 169.254.1.0/30 to 169.254.10.0/30, must be unique
    )
