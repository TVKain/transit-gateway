from taskflow.patterns import linear_flow

from transit.worker.tasks import transit_gateway_peering_attachment


class TransitGatewayPeeringAttachmentFlow:
    def __init__(self):
        pass

    @staticmethod
    def get_transit_gateway_peering_attachment_create_flow():
        tgw_peering_att_create_flow = linear_flow.Flow(
            "transit_peering_attachment_create_flow"
        )

        tgw_peering_att_create_flow.add(
            transit_gateway_peering_attachment.TransitGatewayPeerringAttachmentIDToErrorOnRevertTask()
        )

        tgw_peering_att_create_flow.add(
            transit_gateway_peering_attachment.TransitGatewayPeeringCreateTask()
        )

        tgw_peering_att_create_flow.add(
            transit_gateway_peering_attachment.TransitGatewayPeeringAttachmentUpdateStatusActive()
        )

        return tgw_peering_att_create_flow

    @staticmethod
    def get_transit_gateway_peering_attachment_delete_flow():
        tgw_peering_att_delete_flow = linear_flow.Flow(
            "transit_peering_attachment_delete_flow"
        )

        tgw_peering_att_delete_flow.add(
            transit_gateway_peering_attachment.TransitGatewayPeerringAttachmentIDToErrorOnRevertTask()
        )

        tgw_peering_att_delete_flow.add(
            transit_gateway_peering_attachment.TransitGatewayPeeringDeleteTask()
        )

        tgw_peering_att_delete_flow.add(
            transit_gateway_peering_attachment.TransitGatewayPeeringDeleteInDBTask()
        )

        return tgw_peering_att_delete_flow
