from pydantic import BaseModel, Field, conlist


class InputComputeDriverBuild(BaseModel):
    name: str = Field(default="vytransit")
    vytransit_flavor_id: str
    vytransit_image_id: str
    network_ids: conlist(dict, min_length=1)  # type: ignore


class InputComputeDriverDelete(BaseModel):
    compute_id: str


class InputComputeDriverStatus(BaseModel):
    compute_id: str
