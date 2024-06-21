from sqlmodel import SQLModel


class CreateTransitGatewayVPCRoutesRequest(SQLModel):
    destination_cidr: str
    vpc_attachment_id: str
