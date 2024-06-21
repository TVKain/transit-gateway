from taskflow.patterns import linear_flow

from transit.worker.tasks import vpc_transit_gateway_route


class VPCTransitGatewayRouteFlow:
    def __init__(self):
        pass

    @staticmethod
    def get_vpc_transit_gateway_route_create_flow():
        vpc_tgw_route_create_flow = linear_flow.Flow(
            "vpc_transit_gateway_route_create_flow"
        )

        vpc_tgw_route_create_flow.add(
            vpc_transit_gateway_route.VPCTransitGatewayRouteCreateTask()
        )

        return vpc_tgw_route_create_flow

    @staticmethod
    def get_vpc_transit_gateway_route_delete_flow():
        vpc_tgw_route_delete_flow = linear_flow.Flow(
            "vpc_transit_gateway_route_delete_flow"
        )

        vpc_tgw_route_delete_flow.add(
            vpc_transit_gateway_route.VPCTransitGatewayRouteDeleteTask()
        )

        return vpc_tgw_route_delete_flow
