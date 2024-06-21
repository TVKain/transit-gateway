from typing import Optional
import uuid
from datetime import datetime


from pydantic import ConfigDict
from sqlmodel import Field, SQLModel


class VPCTransitGatewayRouteModel(SQLModel, table=True):
    __tablename__ = "vpc_transit_gateway_routes"
    model_config = ConfigDict(extra="ignore")

    id: str = Field(
        default_factory=lambda: f"vpc-transit-route-{uuid.uuid4()}", primary_key=True
    )

    vpc_id: Optional[str] = None

    target: Optional[str] = Field(foreign_key="transit_gateway_vpc_attachments.id")

    destination: Optional[str]

    status: Optional[str] = None

    created_at: Optional[str] = Field(default_factory=datetime.now)
    updated_at: Optional[str] = Field(default_factory=datetime.now)
