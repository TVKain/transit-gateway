from datetime import datetime

from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict


class TransitGatewayCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    user_id: str


class TransitGatewayCreateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    id: str

    name: str
    user_id: str

    vytransit_id: Optional[str]

    operating_status: Optional[str]
    provisioning_status: Optional[str]

    created_at: datetime
    updated_at: datetime
