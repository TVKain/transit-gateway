from transit.database.adapter import DBAdapter
from transit.database.models.transit_gateway import TransitGatewayModel
from transit.database.repositories.transit_gateway.models.input import (
    TransitGatewayUpdateInput,
)


class TransitGatewayRepository:
    def __init__(self):
        self._db_adapter = DBAdapter()

    def get_all(self):
        try:
            with self._db_adapter.get_session() as session:
                transit_gateways = session.query(TransitGatewayModel).all()
                return [
                    TransitGatewayModel.model_validate(transit_gateway)
                    for transit_gateway in transit_gateways
                ]
        except Exception as e:
            raise e

    def get(self, ident: str):
        try:
            with self._db_adapter.get_session() as session:
                transit_gateway = (
                    session.query(TransitGatewayModel).filter_by(id=ident).first()
                )

                if not transit_gateway:
                    return None
                return TransitGatewayModel.model_validate(transit_gateway)
        except Exception as e:
            raise e

    def create(self, name: str):
        try:
            with self._db_adapter.get_session() as session:
                transit_gateway_model = TransitGatewayModel(name=name, status="BUILD")

                session.add(transit_gateway_model)
                session.commit()

                return TransitGatewayModel.model_validate(transit_gateway_model)
        except Exception as e:
            raise e

    def update(self, update_input: TransitGatewayUpdateInput):
        """Update transit gateway"""

        try:
            with self._db_adapter.get_session() as session:
                transit_gateway = (
                    session.query(TransitGatewayModel)
                    .filter_by(id=update_input.id)
                    .first()
                )

                if update_input.name:
                    transit_gateway.name = update_input.name

                if update_input.compute_id:
                    transit_gateway.compute_id = update_input.compute_id

                if update_input.status:
                    transit_gateway.status = update_input.status

                if update_input.management_ip:
                    transit_gateway.management_ip = update_input.management_ip

                if update_input.vpc_net_ip:
                    transit_gateway.vpc_net_ip = update_input.vpc_net_ip

                if update_input.vpc_net_id:
                    transit_gateway.vpc_net_id = update_input.vpc_net_id

                if update_input.peering_net_ip:
                    transit_gateway.peering_net_ip = update_input.peering_net_ip

                session.commit()

                return TransitGatewayModel.model_validate(transit_gateway)
        except Exception as e:
            raise e

    def delete(self, ident: str):
        pass
