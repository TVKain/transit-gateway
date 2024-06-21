from datetime import datetime

from typing import Optional
import uuid
from pydantic import ConfigDict
from sqlmodel import Field, SQLModel


class TransitGatewayVPCRouteModel(SQLModel, table=True):
    __tablename__ = "transit_gateway_vpc_routes"
    model_config = ConfigDict(extra="ignore")

    id: Optional[str] = Field(
        default_factory=lambda: f"tgw-vpc-route-{uuid.uuid4()}", primary_key=True
    )

    target: Optional[str] = Field(foreign_key="transit_gateway_vpc_attachments.id")
    destination: Optional[str] = None

    status: Optional[str] = None

    created_at: Optional[str] = Field(default_factory=datetime.now)
    updated_at: Optional[str] = Field(default_factory=datetime.now)
