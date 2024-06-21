from typing import Optional
from sqlmodel import Field, SQLModel


class TransitGatewayCreateInput(SQLModel):
    name: Optional[str] = Field(default=None)


class TransitGatewayUpdateInput(SQLModel):
    id: str
    name: Optional[str] = Field(default=None)
    compute_id: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default=None)
    management_ip: Optional[str] = Field(default=None)
    vpc_net_ip: Optional[str] = Field(default=None)
    vpc_net_id: Optional[str] = Field(default=None)
    peering_net_ip: Optional[str] = Field(default=None)
