from sqlalchemy.orm.exc import NoResultFound

from transit.database.adapter import DBAdapter
from transit.database.models.transit_gateway import TransitGatewayModel
from transit.database.models.transit_gateway import TransitGatewaySchema

from transit.database.exceptions import EntityNotFound


class TransitGatewayRepository:
    def __init__(self):
        self._db_adapter = DBAdapter()

    def get(self, ident):
        try:
            with self._db_adapter.get_session() as session:
                transit_gateway_model = session.get_one(
                    TransitGatewayModel, ident=ident
                )

                transit_gateway_data = TransitGatewaySchema.model_validate(
                    transit_gateway_model
                ).model_dump()
        except Exception as _:
            raise EntityNotFound(
                f"Error in get: No transit gateway with id={ident}"
            ) from _

        return transit_gateway_data

    def get_all(self):
        with self._db_adapter.get_session() as session:
            ret = session.query(TransitGatewayModel).all()
            return [TransitGatewaySchema.model_validate(x).model_dump() for x in ret]

    def create(self, **kwargs):
        with self._db_adapter.get_session() as session:
            transit_gateway = TransitGatewayModel(**kwargs)
            session.add(transit_gateway)

            session.commit()

            return TransitGatewaySchema.model_validate(transit_gateway).model_dump()

    def update(self, ident, **kwargs):
        try:
            with self._db_adapter.get_session() as session:
                # Retrieve the TransitGatewayModel record by its identifier
                transit_gateway_db = session.get_one(TransitGatewayModel, ident=ident)

                # Update the record with the provided keyword arguments
                for key, value in kwargs.items():
                    if hasattr(transit_gateway_db, key):
                        setattr(transit_gateway_db, key, value)
                    else:
                        raise ValueError(
                            f"Invalid attribute '{key}' for TransitGatewayModel"
                        )
                return TransitGatewaySchema.model_validate(
                    transit_gateway_db
                ).model_dump()
        except NoResultFound as e:
            raise EntityNotFound(
                f"Error in update: No transit gateway with id={ident}"
            ) from e
