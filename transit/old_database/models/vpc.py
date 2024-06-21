import uuid


from sqlmodel import SQLModel, Field

from pydantic import ConfigDict


# Database model
class VPCModel(SQLModel, table=True):
    __tablename__ = "vpcs"
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=uuid.uuid4, primary_key=True)

    transit_gateway_id: str | None = Field(
        default=None, foreign_key="transit_gateways.id"
    )
