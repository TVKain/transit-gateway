from sqlalchemy.orm.exc import NoResultFound

from transit.database.adapter import DBAdapter
from transit.database.models.transit_gateway_new import (
    TransitGatewayGet,
    TransitGatewayModel,
)

from transit.database.exceptions import EntityNotFound


class TransitGatewayRepository:
    def __init__(self):
        self._db_adapter = DBAdapter()

    def get(self, ident) -> TransitGatewayGet:
        try:
            with self._db_adapter.get_session() as session:
                transit_gateway_model = session.get_one(
                    TransitGatewayModel, ident=ident
                )
        except Exception as _:
            pass
        """try:
            

                transit_gateway_data = TransitGatewaySchema.model_validate(
                    transit_gateway_model
                ).model_dump()
        except Exception as _:
            raise EntityNotFound(
                f"Error in get: No transit gateway with id={ident}"
            ) from _

        return transit_gateway_data"""
