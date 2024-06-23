from transit.database.adapter import DBAdapter

from transit.database.models.transit_gateway_peering_attachment import (
    TransitGatewayPeeringAttachmentModel,
)


class TransitGatewayPeeringAttachmentRepository:
    def __init__(self):
        self._db_adapter = DBAdapter()

    def get(self, ident: str):
        try:
            with self._db_adapter.get_session() as session:
                tgw_peer_attachment = (
                    session.query(TransitGatewayPeeringAttachmentModel)
                    .filter_by(id=ident)
                    .first()
                )

                if not tgw_peer_attachment:
                    return None

                return TransitGatewayPeeringAttachmentModel.model_validate(
                    tgw_peer_attachment
                )
        except Exception as e:
            raise e

    def get_all(self, transit_gateway_id: str | None = None):
        try:
            with self._db_adapter.get_session() as session:
                if transit_gateway_id:
                    tgw_peer_attachments = (
                        session.query(TransitGatewayPeeringAttachmentModel)
                        .filter_by(transit_gateway_id=transit_gateway_id)
                        .all()
                    )
                else:
                    tgw_peer_attachments = session.query(
                        TransitGatewayPeeringAttachmentModel
                    ).all()

                return [
                    TransitGatewayPeeringAttachmentModel.model_validate(
                        tgw_peer_attachment
                    )
                    for tgw_peer_attachment in tgw_peer_attachments
                ]
        except Exception as e:
            raise e

    def create(self, tgw_peer_attachment: TransitGatewayPeeringAttachmentModel):
        try:
            with self._db_adapter.get_session() as session:
                session.add(tgw_peer_attachment)
                session.commit()
                session.refresh(tgw_peer_attachment)
                return TransitGatewayPeeringAttachmentModel.model_validate(
                    tgw_peer_attachment
                )
        except Exception as e:
            print(e)
            raise e

    def update(self, ident: str, status: str):
        try:
            with self._db_adapter.get_session() as session:
                tgw_peer_attachment = (
                    session.query(TransitGatewayPeeringAttachmentModel)
                    .filter_by(id=ident)
                    .first()
                )

                if not tgw_peer_attachment:
                    return None

                tgw_peer_attachment.status = status
                session.commit()
                session.refresh(tgw_peer_attachment)
                return TransitGatewayPeeringAttachmentModel.model_validate(
                    tgw_peer_attachment
                )
        except Exception as e:
            print(e)
            raise e

    def delete(self, ident: str):
        try:
            with self._db_adapter.get_session() as session:
                tgw_peer_attachment = (
                    session.query(TransitGatewayPeeringAttachmentModel)
                    .filter_by(id=ident)
                    .first()
                )

                if not tgw_peer_attachment:
                    return None

                session.delete(tgw_peer_attachment)
                session.commit()
                return True
        except Exception as e:
            print(e)
            raise e
