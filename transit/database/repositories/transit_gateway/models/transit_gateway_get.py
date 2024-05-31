from datetime import datetime

from sqlmodel import SQLModel


class TransitGatewayGetInput(SQLModel):
    id: str


class TransitGatewayGetOutput(SQLModel):
    id: str

    name: str
    user_id: str

    vytransit_id: str

    operating_status: str
    provisioning_status: str

    created_at: datetime
    updated_at: datetime
