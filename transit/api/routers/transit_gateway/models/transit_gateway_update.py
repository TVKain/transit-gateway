from typing import Optional

from datetime import datetime
from pydantic import BaseModel
from pydantic import ConfigDict


class TransitGatewayUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Optional[str]


class TransitGatewayUpdatetResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    id: str

    name: str
    user_id: str

    vytransit_id: Optional[str]  # TODO remove this

    operating_status: Optional[str]
    provisioning_status: Optional[str]

    created_at: datetime
    updated_at: datetime
