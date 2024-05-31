from transit.database.adapter import DBAdapter

from transit.database.models.transit_gateway_new import TransitGatewayModel

from transit.database.repositories.transit_gateway.models.transit_gateway_get import (
    TransitGatewayGetInput,
    TransitGatewayGetOutput,
)


class TransitGatewayRepository:
    def __init__(self):
        self._db_adapter = DBAdapter()

    def get(self, input: TransitGatewayGetInput) -> TransitGatewayGetOutput:
        pass
