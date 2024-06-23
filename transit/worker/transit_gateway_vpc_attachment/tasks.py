from transit.worker.celery_worker import app

from transit.worker.flows.transit_gateway_vpc_attachment import (
    TransitGatewayVPCAttachmentFlow,
)
from transit.worker.run_flow import run_flow


@app.task
def create_transit_gateway_vpc_attachment_task(
    tgw_vpc_att_id: str,
    transit_gateway_id: str,
    vpc_id: str,
    vpc_router_id: str,
    vpc_cidr: str,
    tgw_vpc_net_ip: str,
    tgw_vpc_net_id: str,
    tgw_management_ip: str,
):
    flow = (
        TransitGatewayVPCAttachmentFlow.get_transit_gateway_vpc_attachment_create_flow()
    )

    store = {
        "tgw_vpc_att_id": tgw_vpc_att_id,
        "transit_gateway_id": transit_gateway_id,
        "vpc_id": vpc_id,
        "vpc_router_id": vpc_router_id,
        "vpc_cidr": vpc_cidr,
        "tgw_vpc_net_ip": tgw_vpc_net_ip,
        "tgw_vpc_net_id": tgw_vpc_net_id,
        "tgw_management_ip": tgw_management_ip,
    }

    run_flow(flow=flow, store=store)


@app.task
def delete_transit_gateway_vpc_attachment_task(
    tgw_vpc_att_id: str,
    vpc_router_id: str,
    tgw_vpc_net_id: str,
):
    flow = (
        TransitGatewayVPCAttachmentFlow.get_transit_gateway_vpc_attachment_delete_flow()
    )

    store = {
        "tgw_vpc_att_id": tgw_vpc_att_id,
        "vpc_router_id": vpc_router_id,
        "tgw_vpc_net_id": tgw_vpc_net_id,
    }

    run_flow(flow=flow, store=store)
