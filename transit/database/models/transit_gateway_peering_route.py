import uuid

from typing import Optional

from datetime import datetime

from pydantic import ConfigDict
from sqlmodel import SQLModel, Field


class TransitGatewayPeeringRouteModel(SQLModel, table=True):
    __tablename__ = "transit_gateway_peering_routes"
    model_config = ConfigDict(extra="ignore")

    id: Optional[str] = Field(
        default_factory=lambda: f"tgw-peer-route-{uuid.uuid4()}", primary_key=True
    )

    transit_gateway_peering_attachment_id: Optional[str] = Field(
        foreign_key="transit_gateway_peering_attachments.id"
    )

    destination_cidr: Optional[str] = None

    status: Optional[str] = None

    created_at: Optional[str] = Field(default_factory=datetime.now)
    updated_at: Optional[str] = Field(default_factory=datetime.now)
