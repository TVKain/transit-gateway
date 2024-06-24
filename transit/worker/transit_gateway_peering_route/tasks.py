from transit.worker.celery_worker import app
from transit.worker.flows.transit_gateway_peering_route import (
    TransitGatewayPeeringRouteFlow,
)
from transit.worker.run_flow import run_flow


@app.task
def create_transit_gateway_vpc_attachment_task(
    destination_cidr: str,
    tgw_management_ip: str,
    remote_peering_interface_ip: str,
    tgw_peering_route_id: str,
):
    flow = (
        TransitGatewayPeeringRouteFlow.get_transit_gateway_peering_route_create_flow()
    )

    store = {
        "destination_cidr": destination_cidr,
        "tgw_management_ip": tgw_management_ip,
        "remote_peering_interface_ip": remote_peering_interface_ip,
        "tgw_peering_route_id": tgw_peering_route_id,
    }

    run_flow(flow=flow, store=store)


@app.task
def delete_transit_gateway_peering_attachment_task(
    destination_cidr: str,
    tgw_management_ip: str,
    remote_peering_interface_ip: str,
    tgw_peering_route_id: str,
):
    flow = (
        TransitGatewayPeeringRouteFlow.get_transit_gateway_peering_route_delete_flow()
    )
    store = {
        "destination_cidr": destination_cidr,
        "tgw_management_ip": tgw_management_ip,
        "remote_peering_interface_ip": remote_peering_interface_ip,
        "tgw_peering_route_id": tgw_peering_route_id,
    }

    run_flow(
        flow=flow,
        store=store,
    )
