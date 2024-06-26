from sqlmodel import SQLModel


class CreateTransitGatewayVPCAttachmentRequest(SQLModel):
    name: str | None = None
    transit_gateway_id: str
    vpc_id: str
    vpc_router_id: str
    vpc_cidr: str
