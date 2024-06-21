import uuid
from datetime import datetime

from sqlmodel import SQLModel, Field

from pydantic import ConfigDict


# Database model
class TransitGatewayModel(SQLModel, table=True):
    __tablename__ = "transit_gateways"
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=uuid.uuid4, primary_key=True)

    name: str | None = None
    user_id: str | None = None

    vytransit_id: str | None = None

    operating_status: str | None = None
    provisioning_status: str | None = None

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
