from transit.database.adapter import DBAdapter

from transit.database.models.transit_gateway_vpc_attachment import (
    TransitGatewayVpcAttachmentModel,
)
from transit.database.models.transit_gateway_vpc_route import (
    TransitGatewayVPCRouteModel,
)


class TransitGatewayVPCRouteRepository:
    def __init__(self):
        self._db_adapter = DBAdapter()

    def update(self, ident: str, status: str):
        try:
            with self._db_adapter.get_session() as session:
                tgw_vpc_route = (
                    session.query(TransitGatewayVPCRouteModel)
                    .filter_by(id=ident)
                    .first()
                )

                tgw_vpc_route.status = status

                session.commit()

                return TransitGatewayVPCRouteModel.model_validate(tgw_vpc_route)
        except Exception as e:
            raise e

    def delete(self, ident: str):
        try:
            with self._db_adapter.get_session() as session:
                tgw_vpc_route = (
                    session.query(TransitGatewayVPCRouteModel)
                    .filter_by(id=ident)
                    .first()
                )

                if tgw_vpc_route:
                    session.delete(tgw_vpc_route)
                    session.commit()
        except Exception as e:
            raise e

    def create(
        self, vpc_attachment_id: str, destination_cidr: str, status: str = "PENDING"
    ):
        try:
            with self._db_adapter.get_session() as session:
                tgw_vpc_route = TransitGatewayVPCRouteModel(
                    target=vpc_attachment_id,
                    destination=destination_cidr,
                    status=status,
                )

                session.add(tgw_vpc_route)
                session.commit()

                return TransitGatewayVPCRouteModel.model_validate(tgw_vpc_route)
        except Exception as e:
            raise e

    def get(self, ident: str):
        try:
            with self._db_adapter.get_session() as session:
                tgw_vpc_route = (
                    session.query(TransitGatewayVPCRouteModel)
                    .filter_by(id=ident)
                    .first()
                )

                return TransitGatewayVPCRouteModel.model_validate(tgw_vpc_route)
        except Exception as e:
            raise e

    def get_all_by_tgw_att_id(self, tgw_vpc_att_id: str):
        try:
            with self._db_adapter.get_session() as session:
                tgw_vpc_routes = (
                    session.query(TransitGatewayVPCRouteModel)
                    .filter_by(target=tgw_vpc_att_id)
                    .all()
                )

                return [
                    TransitGatewayVPCRouteModel.model_validate(tgw_vpc_route)
                    for tgw_vpc_route in tgw_vpc_routes
                ]
        except Exception as e:
            raise e

    def get_all_by_tgw_id(self, tgw_id: str):
        try:
            with self._db_adapter.get_session() as session:
                tgw_vpc_atts = (
                    session.query(TransitGatewayVpcAttachmentModel)
                    .filter_by(transit_gateway_id=tgw_id)
                    .all()
                )

                tgw_vpc_routes = []
                for tgw_vpc_att in tgw_vpc_atts:
                    tgw_vpc_routes += (
                        session.query(TransitGatewayVPCRouteModel)
                        .filter_by(target=tgw_vpc_att.id)
                        .all()
                    )

                return [
                    TransitGatewayVPCRouteModel.model_validate(tgw_vpc_route)
                    for tgw_vpc_route in tgw_vpc_routes
                ]
        except Exception as e:
            raise e

    def get_all(self):
        try:
            with self._db_adapter.get_session() as session:

                tgw_vpc_routes = session.query(TransitGatewayVPCRouteModel).all()

                return [
                    TransitGatewayVPCRouteModel.model_validate(tgw_vpc_route)
                    for tgw_vpc_route in tgw_vpc_routes
                ]
        except Exception as e:
            raise e
