import logging

from taskflow import task

from transit.database.repositories.transit_gateway_peering_attachment.transit_gateway_peering_attachment import (
    TransitGatewayPeeringAttachmentRepository,
)


from transit.drivers.vytransit.vytransit_driver import VyTransitDriver

logger = logging.getLogger(__name__)


class TransitGatewayPeerringAttachmentIDToErrorOnRevertTask(task.Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tgw_peer_att_repo = TransitGatewayPeeringAttachmentRepository()

    def execute(self, *args, **kwargs):
        pass

    def revert(self, transit_gateway_peering_attachment_id, *args, **kwargs):

        logger.info(
            f"Reverting TGW Peering Attachment {transit_gateway_peering_attachment_id} to ERROR"
        )

        try:
            self.tgw_peer_att_repo.update(
                ident=transit_gateway_peering_attachment_id,
                status="ERROR",
            )
        except Exception as e:
            print(e)


class TransitGatewayPeeringAttachmentUpdateStatusActive(task.Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tgw_peer_att_repo = TransitGatewayPeeringAttachmentRepository()

    def execute(self, transit_gateway_peering_attachment_id, *args, **kwargs):

        self.tgw_peer_att_repo.update(
            ident=transit_gateway_peering_attachment_id,
            status="ACTIVE",
        )

    def revert(self, *args, **kwargs):
        pass


class TransitGatewayPeeringCreateTask(task.Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tgw_peer_att_repo = TransitGatewayPeeringAttachmentRepository()

    def execute(
        self,
        tgw_management_ip,
        tunnel_interface_ip,
        remote_tunnel_interface_ip,
        tun_num,
        tun_ip,
        *args,
        **kwargs,
    ):
        vytransit_driver = VyTransitDriver(tgw_management_ip)

        vytransit_driver.add_tunnel(
            tunnel_interface_ip=tunnel_interface_ip,
            remote_tunnel_interface_ip=remote_tunnel_interface_ip,
            tun_num=tun_num,
            tun_ip=tun_ip,
        )

    def revert(self, *args, **kwargs):

        pass


class TransitGatewayPeeringDeleteTask(task.Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tgw_peer_att_repo = TransitGatewayPeeringAttachmentRepository()

    def execute(self, tgw_management_ip, tun_num, *args, **kwargs):
        vytransit_driver = VyTransitDriver(tgw_management_ip)

        vytransit_driver.remove_tunnel(
            tun_num=tun_num,
        )

    def revert(self, *args, **kwargs):
        pass


class TransitGatewayPeeringDeleteInDBTask(task.Task):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tgw_peer_att_repo = TransitGatewayPeeringAttachmentRepository()

    def execute(self, transit_gateway_peering_attachment_id, *args, **kwargs):
        self.tgw_peer_att_repo.delete(transit_gateway_peering_attachment_id)

    def revert(self, *args, **kwargs):
        pass
