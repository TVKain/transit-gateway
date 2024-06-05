from pydantic import BaseModel


class NetworkDriverDetachRouterFromSubnetInput(BaseModel):
    router_id: str
    subnet_id: str
