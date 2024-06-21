from sqlmodel import SQLModel


class TransitGatewayCreateOutput(SQLModel):
    id: str
    name: str
    compute_id: str
    status: str
