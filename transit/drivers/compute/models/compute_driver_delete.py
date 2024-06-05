from pydantic import BaseModel


class ComputeDriverDeleteInput(BaseModel):
    compute_id: str
