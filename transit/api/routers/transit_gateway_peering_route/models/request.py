from sqlmodel import SQLModel


class TransitGatewayPeeringAttachmentCreateRouteRequest(SQLModel):

    destination_cidr: str
    transit_gateway_peering_attachment_id: str
