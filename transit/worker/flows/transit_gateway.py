from taskflow.patterns import linear_flow

from transit.worker.tasks import transit_gateway


class TransitGatewayFlow:
    def __init__(self):
        pass

    @staticmethod
    def get_transit_gateway_create_flow():
        transit_gateway_create_flow = linear_flow.Flow("transit_create_flow")

        transit_gateway_create_flow.add(
            transit_gateway.TransitGatewayIDToErrorOnRevertTask(
                requires="transit_gateway_id"
            )
        )

        transit_gateway_create_flow.add(
            transit_gateway.TransitGatewayCreateNetwork(
                requires="transit_gateway_id", provides="vpc_network_id"
            )
        )

        transit_gateway_create_flow.add(
            transit_gateway.TransitGatewayComputeBuildTask(
                requires=("transit_gateway_id", "vpc_network_id"),
                provides="vytransit_id",
            )
        )

        transit_gateway_create_flow.add(
            transit_gateway.TransitGatewayMarkActiveInDB(
                requires=("transit_gateway_id", "vytransit_id")
            )
        )

        return transit_gateway_create_flow

    @staticmethod
    def get_transit_gateway_delete_flow():
        transit_gateway_delete_flow = linear_flow.Flow("transit_delete_flow")

        transit_gateway_delete_flow.add(
            transit_gateway.TransitGatewayIDToErrorOnRevertTask(
                requires="transit_gateway_id"
            )
        )

        transit_gateway_delete_flow.add(
            transit_gateway.TransitGatewayDeleteComputeTask(requires="compute_id")
        )

        transit_gateway_delete_flow.add(
            transit_gateway.TransitGatewayDeleteNetworkTask(requires="vpc_net_id")
        )

        transit_gateway_delete_flow.add(
            transit_gateway.TransitGatewayDeleteTransitInDBTask(
                requires="transit_gateway_id"
            )
        )

        return transit_gateway_delete_flow
