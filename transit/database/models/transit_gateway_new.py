import uuid
from datetime import datetime

from sqlmodel import SQLModel, Field


# Database model
class TransitGatewayModel(SQLModel, table=True):
    __tablename__ = "transit_gateways"
    id: str = Field(default_factory=uuid.uuid4, primary_key=True)

    name: str
    user_id: str

    vytransit_id: str

    operating_status: str
    provisioning_status: str

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class TransitGatewayCreate(SQLModel):
    name: str
    user_id: str


class TranstiGatewayUpdate(SQLModel):
    name: str


class TransitGatewayGet(SQLModel):
    id: str

    name: str
    user_id: str

    vytransit_id: str

    operating_status: str
    provisioning_status: str

    created_at: datetime
    updated_at: datetime
