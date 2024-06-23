from transit.worker.celery_worker import app

from transit.worker.flows.transit_gateway import TransitGatewayFlow
from transit.worker.run_flow import run_flow


@app.task
def create_transit_gateway_task(transit_gateway_id: str):
    flow = TransitGatewayFlow.get_transit_gateway_create_flow()

    store = {
        "transit_gateway_id": transit_gateway_id,
    }

    run_flow(flow=flow, store=store)


@app.task
def delete_transit_gateway_task(
    transit_gateway_id: str, compute_id: str, vpc_net_id: str
):
    flow = TransitGatewayFlow.get_transit_gateway_delete_flow()

    store = {
        "transit_gateway_id": transit_gateway_id,
        "compute_id": compute_id,
        "vpc_net_id": vpc_net_id,
    }

    run_flow(flow=flow, store=store)
