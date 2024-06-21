from taskflow.patterns import linear_flow

from transit.worker.tasks import transit_gateway_vpc_attachment

from transit.worker.tasks import transit_gateway_vpc_route


class TransitGatewayVPCRouteFlow:
    def __init__(self):
        pass

    @staticmethod
    def get_transit_gateway_vpc_route_create_flow():
        tgw_vpc_route_create_flow = linear_flow.Flow("transit_vpc_route_create_flow")

        tgw_vpc_route_create_flow.add(
            transit_gateway_vpc_route.TransitGatewayVPCRouteIDToErrorOnRevertTask()
        )

        tgw_vpc_route_create_flow.add(
            transit_gateway_vpc_route.TransitGatewayVPCRouteCreateTask()
        )

        return tgw_vpc_route_create_flow

    @staticmethod
    def get_transit_gateway_vpc_route_delete_flow():
        tgw_vpc_route_delete_flow = linear_flow.Flow("transit_vpc_route_delete_flow")

        tgw_vpc_route_delete_flow.add(
            transit_gateway_vpc_route.TransitGatewayVPCRouteIDToErrorOnRevertTask()
        )

        tgw_vpc_route_delete_flow.add(
            transit_gateway_vpc_route.TransitGatewayVPCRouteDeleteTask()
        )

        return tgw_vpc_route_delete_flow
