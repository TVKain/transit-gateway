from pydantic import BaseModel, Field, conlist


class ComputeDriverBuildInput(BaseModel):
    name: str = Field(default="vytransit")
    vytransit_flavor_id: str
    vytransit_image_id: str
    network_ids: conlist(dict, min_length=1)  # type: ignore
