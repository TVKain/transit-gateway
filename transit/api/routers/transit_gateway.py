from fastapi import APIRouter
from sqlmodel import SQLModel

router = APIRouter(prefix="/transit-gateways", tags=["transit-gateways"])


class Test(SQLModel):
    hi: str


@router.get("/", response_model=Test)
def test():
    return Test(hi="hi")
