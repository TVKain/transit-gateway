from datetime import datetime


from sqlmodel import SQLModel, Field

from pydantic import ConfigDict


# Database model
class TransitGatewayPeeringModel(SQLModel, table=True):
    __tablename__ = "transit_gateway_peerings"
    model_config = ConfigDict(extra="ignore")
    transit_gateway_first_id: str = Field(
        primary_key=True, foreign_key="transit_gateways.id"
    )
    transit_gateway_second_id: str = Field(
        primary_key=True, foreign_key="transit_gateways.id"
    )

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
