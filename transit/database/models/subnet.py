import uuid


from sqlmodel import SQLModel, Field

from pydantic import ConfigDict


# Database model
class SubnetModel(SQLModel, table=True):
    __tablename__ = "subnets"
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=uuid.uuid4, primary_key=True)
    address: str
    vpc_id: str | None = Field(default=None, foreign_key="vpcs.id")
