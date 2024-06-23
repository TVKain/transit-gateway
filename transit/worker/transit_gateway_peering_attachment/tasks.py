from transit.worker.celery_worker import app

from transit.worker.flows.transit_gateway_peering_attachment import (
    TransitGatewayPeeringAttachmentFlow,
)
from transit.worker.run_flow import run_flow


@app.task
def create_transit_gateway_peering_attachment_task(
    transit_gateway_peering_attachment_id: str,
    tun_num: int,
    tun_ip: str,
    tunnel_interface_ip: str,
    remote_tunnel_interface_ip: str,
    tgw_management_ip: str,
):
    flow = (
        TransitGatewayPeeringAttachmentFlow.get_transit_gateway_peering_attachment_create_flow()
    )

    store = {
        "transit_gateway_peering_attachment_id": transit_gateway_peering_attachment_id,
        "tun_num": tun_num,
        "tun_ip": tun_ip,
        "tunnel_interface_ip": tunnel_interface_ip,
        "remote_tunnel_interface_ip": remote_tunnel_interface_ip,
        "tgw_management_ip": tgw_management_ip,
    }

    run_flow(flow=flow, store=store)


@app.task
def delete_transit_gateway_peering_attachment_task(
    transit_gateway_peering_attachment_id: str,
    tun_num: int,
    tgw_management_ip: str,
):
    flow = (
        TransitGatewayPeeringAttachmentFlow.get_transit_gateway_peering_attachment_delete_flow()
    )

    store = {
        "transit_gateway_peering_attachment_id": transit_gateway_peering_attachment_id,
        "tun_num": tun_num,
        "tgw_management_ip": tgw_management_ip,
    }

    run_flow(flow=flow, store=store)
