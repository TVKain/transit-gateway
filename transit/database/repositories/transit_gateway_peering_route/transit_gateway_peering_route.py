from transit.database.adapter import DBAdapter

from transit.database.models.transit_gateway_peering_attachment import (
    TransitGatewayPeeringAttachmentModel,
)
from transit.database.models.transit_gateway_peering_route import (
    TransitGatewayPeeringRouteModel,
)


class TransitGatewayPeeringRouteRepository:
    def __init__(self):
        self._db_adapter = DBAdapter()

    def get(self, ident: str):
        try:
            with self._db_adapter.get_session() as session:
                tgw_peer_route = (
                    session.query(TransitGatewayPeeringRouteModel)
                    .filter_by(id=ident)
                    .first()
                )

                if not tgw_peer_route:
                    return None

                return TransitGatewayPeeringRouteModel.model_validate(tgw_peer_route)
        except Exception as e:
            raise e

    def get_all_by_transit_gateway_id(self, transit_gateway_id: str):
        try:
            with self._db_adapter.get_session() as session:
                tgw_peer_atts = (
                    session.query(TransitGatewayPeeringAttachmentModel)
                    .filter_by(transit_gateway_id=transit_gateway_id)
                    .all()
                )

                tgw_peering_routes = []

                for tgw_peer_att in tgw_peer_atts:
                    tgw_peering_routes += (
                        session.query(TransitGatewayPeeringRouteModel)
                        .filter_by(
                            transit_gateway_peering_attachment_id=tgw_peer_att.id
                        )
                        .all()
                    )

                return [
                    TransitGatewayPeeringRouteModel.model_validate(tgw_peering_route)
                    for tgw_peering_route in tgw_peering_routes
                ]
        except Exception as e:
            raise e

    def get_all(self, transit_gateway_peering_attachment_id: str | None = None):
        try:
            with self._db_adapter.get_session() as session:
                if transit_gateway_peering_attachment_id:
                    tgw_peer_attachments = (
                        session.query(TransitGatewayPeeringRouteModel)
                        .filter_by(
                            transit_gateway_peering_attachment_id=transit_gateway_peering_attachment_id
                        )
                        .all()
                    )
                else:
                    tgw_peer_attachments = session.query(
                        TransitGatewayPeeringRouteModel
                    ).all()

                return [
                    TransitGatewayPeeringRouteModel.model_validate(tgw_peer_attachment)
                    for tgw_peer_attachment in tgw_peer_attachments
                ]
        except Exception as e:
            raise e

    def create(
        self,
        transit_gateway_peering_attachment_id: str,
        destination_cidr: str,
        status: str,
    ):
        try:
            with self._db_adapter.get_session() as session:
                tgw_peer_route = TransitGatewayPeeringRouteModel(
                    transit_gateway_peering_attachment_id=transit_gateway_peering_attachment_id,
                    destination_cidr=destination_cidr,
                    status=status,
                )

                session.add(tgw_peer_route)
                session.commit()

                return TransitGatewayPeeringRouteModel.model_validate(tgw_peer_route)
        except Exception as e:
            raise e from e

    def update(self, ident: str, status: str):
        try:
            with self._db_adapter.get_session() as session:
                tgw_peer_attachment = (
                    session.query(TransitGatewayPeeringRouteModel)
                    .filter_by(id=ident)
                    .first()
                )

                if not tgw_peer_attachment:
                    return None

                tgw_peer_attachment.status = status
                session.commit()
                session.refresh(tgw_peer_attachment)
                return TransitGatewayPeeringRouteModel.model_validate(
                    tgw_peer_attachment
                )
        except Exception as e:
            print(e)
            raise e

    def delete(self, ident: str):
        try:
            with self._db_adapter.get_session() as session:
                tgw_peer_route = (
                    session.query(TransitGatewayPeeringRouteModel)
                    .filter_by(id=ident)
                    .first()
                )

                if not tgw_peer_route:
                    return None

                session.delete(tgw_peer_route)
                session.commit()
                return True
        except Exception as e:
            print(e)
            raise e
