from taskflow.patterns import linear_flow

from transit.worker.tasks import transit_gateway_vpc_attachment


class TransitGatewayVPCAttachmentFlow:
    def __init__(self):
        pass

    @staticmethod
    def get_transit_gateway_vpc_attachment_create_flow():
        tgw_vpc_att_create_flow = linear_flow.Flow("transit_vpc_attachment_create_flow")

        tgw_vpc_att_create_flow.add(
            transit_gateway_vpc_attachment.TransitGatewayVPCAttachmentIDToErrorOnRevertTask()
        )

        tgw_vpc_att_create_flow.add(
            transit_gateway_vpc_attachment.TransitGatewayVPCAttachmentAttachRouterToTGWNet(
                provides="vpc_router_info"
            ),
        )

        # Remove this for now
        # tgw_vpc_att_create_flow.add(
        #     transit_gateway_vpc_attachment.TransitGatewayVPCAttachmentAddRouteIfPossible(
        #         requires="vpc_router_info"
        #     )
        # )

        return tgw_vpc_att_create_flow

    @staticmethod
    def get_transit_gateway_vpc_attachment_delete_flow():
        tgw_vpc_att_delete_flow = linear_flow.Flow("transit_vpc_attachment_delete_flow")

        tgw_vpc_att_delete_flow.add(
            transit_gateway_vpc_attachment.TransitGatewayVPCAttachmentIDToErrorOnRevertTask()
        )

        tgw_vpc_att_delete_flow.add(
            transit_gateway_vpc_attachment.TransitGatewayVPCAttachmentDetachRouterFromTGWNet()
        )

        tgw_vpc_att_delete_flow.add(
            transit_gateway_vpc_attachment.TransitGatewayVPCAttachmentDeleteAttachmentFromDB()
        )

        return tgw_vpc_att_delete_flow
