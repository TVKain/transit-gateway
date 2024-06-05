from pydantic import BaseModel


class NetworkDriverSubnet(BaseModel):
    id: str
    network_id: str
    address: str


class NetworkDriverGetSubnetsInput(BaseModel):
    network_id: str


class NetworkDriverGetSubnetsOutput(BaseModel):
    subnets: list[NetworkDriverSubnet]
