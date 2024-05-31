from typing import Optional

from pydantic import BaseModel


class RequestTransitGatewayPost(BaseModel):
    user_id: str
    name: str


class RequestTransitGatewayPatch(BaseModel):
    name: Optional[str]
