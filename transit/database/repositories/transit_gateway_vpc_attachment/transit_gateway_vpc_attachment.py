from transit.database.adapter import DBAdapter
from transit.database.models.transit_gateway_vpc_attachment import (
    TransitGatewayVpcAttachmentModel,
)
from transit.database.repositories.transit_gateway_vpc_attachment.models.input import (
    TransitGatewayVPCAttachmentCreateInput,
    TransitGatewayVPCAttachmentUpdateInput,
)


class TransitGatewayVPCAttachmentRepository:
    def __init__(self):
        self._db_adapter = DBAdapter()

    def get_by_vpc_id(self, vpc_id: str):
        try:
            with self._db_adapter.get_session() as session:
                tgw_vpc_attachment = (
                    session.query(TransitGatewayVpcAttachmentModel)
                    .filter_by(vpc_id=vpc_id)
                    .first()
                )

                if tgw_vpc_attachment:

                    return TransitGatewayVpcAttachmentModel.model_validate(
                        tgw_vpc_attachment
                    )
                else:
                    return None
        except Exception as e:
            raise e

    def get(self, ident: str):
        try:
            with self._db_adapter.get_session() as session:
                tgw_vpc_attachment = (
                    session.query(TransitGatewayVpcAttachmentModel)
                    .filter_by(id=ident)
                    .first()
                )

                return TransitGatewayVpcAttachmentModel.model_validate(
                    tgw_vpc_attachment
                )
        except Exception as e:
            raise e

    def get_all(self, transit_gateway_id: str | None = None):
        try:
            with self._db_adapter.get_session() as session:

                if transit_gateway_id:
                    tgw_vpc_attachments = (
                        session.query(TransitGatewayVpcAttachmentModel)
                        .filter_by(transit_gateway_id=transit_gateway_id)
                        .all()
                    )
                else:
                    tgw_vpc_attachments = session.query(
                        TransitGatewayVpcAttachmentModel
                    ).all()

                return [
                    TransitGatewayVpcAttachmentModel.model_validate(tgw_vpc_attachment)
                    for tgw_vpc_attachment in tgw_vpc_attachments
                ]
        except Exception as e:
            raise e

    def create(self, create_input: TransitGatewayVPCAttachmentCreateInput):
        try:
            with self._db_adapter.get_session() as session:
                transit_gateway_vpc_attachment_model = TransitGatewayVpcAttachmentModel(
                    name=create_input.name,
                    transit_gateway_id=create_input.transit_gateway_id,
                    vpc_id=create_input.vpc_id,
                    vpc_router_id=create_input.vpc_router_id,
                    vpc_cidr=create_input.vpc_cidr,
                    status=create_input.status,
                )

                session.add(transit_gateway_vpc_attachment_model)
                session.commit()

                return TransitGatewayVpcAttachmentModel.model_validate(
                    transit_gateway_vpc_attachment_model
                )
        except Exception as e:
            raise e

    def update(self, update_input: TransitGatewayVPCAttachmentUpdateInput):
        """Update transit gateway"""

        try:
            with self._db_adapter.get_session() as session:
                attachment = (
                    session.query(TransitGatewayVpcAttachmentModel)
                    .filter_by(id=update_input.id)
                    .first()
                )

                if update_input.name:
                    attachment.name = update_input.name

                if update_input.status:
                    attachment.status = update_input.status

                if update_input.vpc_net_ip:
                    attachment.vpc_net_ip = update_input.vpc_net_ip

                if update_input.vpc_net_port_id:
                    attachment.vpc_net_port_id = update_input.vpc_net_port_id

                session.commit()

                return TransitGatewayVpcAttachmentModel.model_validate(attachment)
        except Exception as e:
            raise e

    def delete(self, ident: str):
        try:
            with self._db_adapter.get_session() as session:
                session.query(TransitGatewayVpcAttachmentModel).filter_by(
                    id=ident
                ).delete()
                session.commit()

        except Exception as e:
            raise e
