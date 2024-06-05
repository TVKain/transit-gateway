from pydantic import BaseModel


class ComputeDriverStatusInput(BaseModel):
    compute_id: str
