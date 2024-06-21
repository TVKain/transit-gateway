from sqlmodel import SQLModel


class TransitGatewayGetResponse(SQLModel):
    id: str
    name: str
    status: str


class TransitGatewayCreateResponse(SQLModel):
    id: str
    name: str
    status: str
