from transit.old_database.adapter import DBAdapter

from transit.old_database.models.transit_gateway import TransitGatewayModel

from transit.old_database.repositories.transit_gateway.models.transit_gateway_get import (
    TransitGatewayGetInput,
    TransitGatewayGetOutput,
)

from transit.old_database.repositories.transit_gateway.models.transit_gateway_create import (
    TransitGatewayCreateInput,
    TransitGatewayCreateOutput,
)

from transit.old_database.repositories.transit_gateway.models.transit_gateway_update import (
    TransitGatewayUpdateInput,
    TransitGatewayUpdatetOutput,
)


class TransitGatewayRepository:
    def __init__(self):
        self._db_adapter = DBAdapter()

    def get_all(self) -> list[TransitGatewayGetOutput]:
        try:
            with self._db_adapter.get_session() as session:
                transit_gateways_db = session.query(TransitGatewayModel).all()

                get_output = [
                    TransitGatewayGetOutput.model_validate(x)
                    for x in transit_gateways_db
                ]

        except Exception as e:
            print(e)

        return get_output

    def get(self, get_input: TransitGatewayGetInput) -> TransitGatewayGetOutput:

        try:
            with self._db_adapter.get_session() as session:
                transit_gateway_db = session.get_one(
                    TransitGatewayModel, ident=get_input.id
                )

                get_output = TransitGatewayGetOutput.model_validate(transit_gateway_db)

        except Exception as e:
            print(e)

        return get_output

    def create(
        self, create_input: TransitGatewayCreateInput
    ) -> TransitGatewayCreateOutput:

        try:
            with self._db_adapter.get_session() as session:

                transit_gateway_db = TransitGatewayModel(
                    user_id=create_input.user_id, name=create_input.name
                )

                session.add(transit_gateway_db)
                session.commit()

                transit_gateway_output = TransitGatewayCreateOutput.model_validate(
                    transit_gateway_db
                )

        except Exception as e:
            print(e)
        return transit_gateway_output

    def update(
        self, update_input: TransitGatewayUpdateInput
    ) -> TransitGatewayUpdatetOutput:
        try:
            with self._db_adapter.get_session() as session:
                transit_gateway_db = session.get_one(
                    TransitGatewayModel, ident=update_input.id
                )

                transit_gateway_db.name = update_input.name or transit_gateway_db.name
                transit_gateway_db.vytransit_id = (
                    update_input.vytransit_id or transit_gateway_db.vytransit_id
                )
                transit_gateway_db.operating_status = (
                    update_input.operating_status or transit_gateway_db.operating_status
                )
                transit_gateway_db.provisioning_status = (
                    update_input.provisioning_status
                    or transit_gateway_db.provisioning_status
                )

                session.commit()

                update_output = TransitGatewayUpdatetOutput.model_validate(
                    transit_gateway_db
                )
        except Exception as e:
            print(e)
        return update_output
