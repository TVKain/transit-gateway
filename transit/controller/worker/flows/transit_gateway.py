from taskflow.patterns import linear_flow

from transit.controller.worker.tasks import transit_gateway


class TransitGatewayFlow:
    def __init__(self):
        pass

    @staticmethod
    def get_transit_gateway_create_flow():
        transit_gateway_create_flow = linear_flow.Flow("test")

        transit_gateway_create_flow.add(
            transit_gateway.TransitGatewayIDToErrorOnRevertTask(
                requires="transit_gateway_id"
            )
        )

        transit_gateway_create_flow.add(
            transit_gateway.ComputeBuildTask(
                requires="transit_gateway_id", provides="vytransit_id"
            )
        )

        transit_gateway_create_flow.add(
            transit_gateway.TransitGatewayMarkReadyInDB(
                requires=("transit_gateway_id", "vytransit_id")
            )
        )

        return transit_gateway_create_flow
