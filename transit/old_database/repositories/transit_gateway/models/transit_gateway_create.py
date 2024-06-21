from typing import Optional

from datetime import datetime


from pydantic import BaseModel

from pydantic import ConfigDict


class TransitGatewayCreateInput(BaseModel):
    user_id: str
    name: str


class TransitGatewayCreateOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="ignore")

    id: str

    name: str
    user_id: str

    vytransit_id: Optional[str]  # TODO: Remove optional

    operating_status: Optional[str]
    provisioning_status: Optional[str]

    created_at: datetime
    updated_at: datetime
