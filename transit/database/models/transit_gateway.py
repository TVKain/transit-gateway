from datetime import datetime
import uuid

from typing import Optional
from pydantic import ConfigDict
from sqlmodel import Field, SQLModel


class TransitGatewayModel(SQLModel, table=True):
    __tablename__ = "transit_gateways"
    model_config = ConfigDict(extra="ignore")

    id: Optional[str] = Field(
        default_factory=lambda: f"tgw-{uuid.uuid4()}", primary_key=True
    )
    name: Optional[str] = None

    compute_id: Optional[str] = None
    status: Optional[str] = None
    management_ip: Optional[str] = None
    vpc_net_ip: Optional[str] = None
    vpc_net_id: Optional[str] = None
    peering_net_ip: Optional[str] = None

    created_at: Optional[str] = Field(default_factory=datetime.now)
    updated_at: Optional[str] = Field(default_factory=datetime.now)
