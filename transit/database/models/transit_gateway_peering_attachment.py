import uuid

from typing import Optional
from sqlmodel import SQLModel, Field

from pydantic import ConfigDict


class TransitGatewayPeeringAttachmentModel(SQLModel):
    __tablename__ = "transit_gateway_peering_attachments"
    model_config = ConfigDict(extra="ignore")

    id: Optional[str] = Field(
        default_factory=lambda: f"tgw-peer-att-{uuid.uuid4()}", primary_key=True
    )

    transit_gateway_id: Optional[str] = Field(foreign_key="transit_gateways.id")
    tunnel_interface_ip: Optional[str] = None
    remote_peering_interface_ip: Optional[str] = None
    remote_transit_gateway_id: Optional[str] = None
