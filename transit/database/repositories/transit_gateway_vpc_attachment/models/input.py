from sqlmodel import SQLModel


class TransitGatewayVPCAttachmentCreateInput(SQLModel):
    transit_gateway_id: str
    vpc_id: str
    vpc_router_id: str
    vpc_cidr: str
    status: str


class TransitGatewayVPCAttachmentUpdateInput(SQLModel):
    id: str
    status: str | None = None

    vpc_net_ip: str | None = None
    vpc_net_port_id: str | None = None
