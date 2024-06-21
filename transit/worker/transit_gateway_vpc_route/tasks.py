from transit.worker.celery_worker import app

from transit.worker.flows.transit_gateway_vpc_route import (
    TransitGatewayVPCRouteFlow,
)
from transit.worker.run_flow import run_flow


@app.task
def create_transit_gateway_vpc_route_task(
    tgw_vpc_route_id: str,
    tgw_vpc_att_id: str,
    destination_cidr: str,
):
    flow = TransitGatewayVPCRouteFlow.get_transit_gateway_vpc_route_create_flow()

    store = {
        "tgw_vpc_route_id": tgw_vpc_route_id,
        "tgw_vpc_att_id": tgw_vpc_att_id,
        "destination_cidr": destination_cidr,
    }

    run_flow(flow=flow, store=store)


@app.task
def delete_transit_gateway_vpc_route_task(
    tgw_vpc_route_id, vpc_net_ip, tgw_management_ip, destination_cidr
):
    flow = TransitGatewayVPCRouteFlow.get_transit_gateway_vpc_route_delete_flow()

    run_flow(
        flow=flow,
        store={
            "tgw_vpc_route_id": tgw_vpc_route_id,
            "vpc_net_ip": vpc_net_ip,
            "destination_cidr": destination_cidr,
            "tgw_management_ip": tgw_management_ip,
        },
    )
