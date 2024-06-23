from typing import Optional
from sqlmodel import SQLModel


class TransitGatewayPeeringAttachmentCreateInput(SQLModel):
    transit_gateway_id: str

    tunnel_interface_ip: str
    remote_peering_interface_ip: str

    remote_transit_gateway_id: str

    vti_num: Optional[int] = None
    vti_ip: Optional[str] = None
