from transit.worker.celery_worker import app

from transit.worker.flows.vpc_transit_gateway_route import (
    VPCTransitGatewayRouteFlow,
)
from transit.worker.run_flow import run_flow


@app.task
def create_vpc_transit_gateway_route_task(
    vpc_router_id: str,
    destination_cidr: str,
    tgw_vpc_net_ip: str,
    vpc_tgw_route_id: str,
):
    flow = VPCTransitGatewayRouteFlow.get_vpc_transit_gateway_route_create_flow()

    store = {
        "vpc_tgw_route_id": vpc_tgw_route_id,
        "vpc_router_id": vpc_router_id,
        "destination_cidr": destination_cidr,
        "tgw_vpc_net_ip": tgw_vpc_net_ip,
    }

    run_flow(flow=flow, store=store)


@app.task
def delete_vpc_transit_gateway_route_task(
    vpc_router_id: str,
    vpc_tgw_route_id: str,
    destination_cidr: str,
    tgw_vpc_net_ip: str,
):
    flow = VPCTransitGatewayRouteFlow.get_vpc_transit_gateway_route_delete_flow()

    store = {
        "vpc_tgw_route_id": vpc_tgw_route_id,
        "vpc_router_id": vpc_router_id,
        "destination_cidr": destination_cidr,
        "tgw_vpc_net_ip": tgw_vpc_net_ip,
    }

    run_flow(flow=flow, store=store)
