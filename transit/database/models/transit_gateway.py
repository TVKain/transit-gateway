# pylint: disable=not-callable

import uuid
import datetime

from typing import Optional

from pydantic import BaseModel, ConfigDict


from sqlalchemy import String, Column, DateTime
from sqlalchemy.sql import func

from transit.database.models.base import Base


class TransitGatewayModel(Base):
    __tablename__ = "transit_gateways"
    id: str = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: str = Column(String(255))
    user_id: str = Column(String(255))

    vytransit_id: str = Column(String(64))

    operating_status: str = Column(String(16))
    provisioning_status: str = Column(String(16))

    created_at: datetime.datetime = Column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: datetime.datetime = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class TransitGatewaySchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    user_id: str

    operating_status: Optional[str]
    provisioning_status: Optional[str]

    created_at: datetime.datetime
    updated_at: datetime.datetime
