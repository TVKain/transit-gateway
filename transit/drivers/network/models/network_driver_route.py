from pydantic import BaseModel


class NetworkDriverRoute(BaseModel):
    destination: str
    next_hop: str
