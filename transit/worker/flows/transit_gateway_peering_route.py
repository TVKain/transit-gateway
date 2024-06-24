from taskflow.patterns import linear_flow

from transit.worker.tasks import transit_gateway_peering_route


class TransitGatewayPeeringRouteFlow:
    def __init__(self):
        pass

    @staticmethod
    def get_transit_gateway_peering_route_create_flow():
        tgw_peering_att_create_flow = linear_flow.Flow(
            "transit_peering_route_create_flow"
        )

        tgw_peering_att_create_flow.add(
            transit_gateway_peering_route.TransitGatewayPeerringRouteIDToErrorOnRevertTask()
        )

        tgw_peering_att_create_flow.add(
            transit_gateway_peering_route.TransitGatewayPeeringRouteCreateTask()
        )

        return tgw_peering_att_create_flow

    @staticmethod
    def get_transit_gateway_peering_route_delete_flow():
        tgw_peering_att_delete_flow = linear_flow.Flow(
            "transit_peering_route_delete_flow"
        )

        tgw_peering_att_delete_flow.add(
            transit_gateway_peering_route.TransitGatewayPeerringRouteIDToErrorOnRevertTask()
        )

        tgw_peering_att_delete_flow.add(
            transit_gateway_peering_route.TransitGatewayPeeringRouteDeleteTask()
        )

        return tgw_peering_att_delete_flow
