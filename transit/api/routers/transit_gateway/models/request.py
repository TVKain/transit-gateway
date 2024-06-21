from typing import Optional
from sqlmodel import SQLModel


class TransitGatewayCreateRequest(SQLModel):
    name: Optional[str] = None
