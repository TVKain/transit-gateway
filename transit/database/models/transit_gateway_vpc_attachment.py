from datetime import datetime

from typing import Optional
import uuid
from pydantic import ConfigDict
from sqlmodel import Field, SQLModel


class TransitGatewayVpcAttachmentModel(SQLModel, table=True):
    __tablename__ = "transit_gateway_vpc_attachments"
    model_config = ConfigDict(extra="ignore")

    id: Optional[str] = Field(
        default_factory=lambda: f"tgw-vpc-att-{uuid.uuid4()}", primary_key=True
    )

    name: Optional[str] = None

    vpc_id: Optional[str] = None
    vpc_cidr: Optional[str] = None
    vpc_router_id: Optional[str] = None
    status: Optional[str] = None

    vpc_net_ip: Optional[str] = None
    vpc_net_port_id: Optional[str] = None

    transit_gateway_id: Optional[str] = Field(foreign_key="transit_gateways.id")

    created_at: Optional[str] = Field(default_factory=datetime.now)
    updated_at: Optional[str] = Field(default_factory=datetime.now)
