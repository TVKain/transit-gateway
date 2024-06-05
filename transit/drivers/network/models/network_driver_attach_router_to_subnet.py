from pydantic import BaseModel


class NetworkDriverAttachRouterToSubnetInput(BaseModel):
    router_id: str
    subnet_id: str


class NetworkDriverAttachRouterToSubnetOutput(BaseModel):
    router_id: str
    subnet_id: str
    ip_address: str
