import ipaddress
from transit.database.repositories.transit_gateway_peering_attachment.transit_gateway_peering_attachment import (
    TransitGatewayPeeringAttachmentRepository,
)
from transit.database.repositories.transit_gateway_peering_route.transit_gateway_peering_route import (
    TransitGatewayPeeringRouteRepository,
)
from transit.database.repositories.transit_gateway_vpc_attachment.transit_gateway_vpc_attachment import (
    TransitGatewayVPCAttachmentRepository,
)
from transit.database.repositories.transit_gateway_vpc_route.transit_gateway_vpc_route import (
    TransitGatewayVPCRouteRepository,
)


def check_tgw_route_overlap(tgw_id: str, destination_cidr: str):
    tgw_vpc_route_repo = TransitGatewayVPCRouteRepository()

    tgw_vpc_att_repo = TransitGatewayVPCAttachmentRepository()

    tgw_peering_route_repo = TransitGatewayPeeringRouteRepository()

    tgw_peering_att_repo = TransitGatewayPeeringAttachmentRepository()

    tgw_vpc_atts = tgw_vpc_att_repo.get_all(tgw_id)

    destination_cidr_ip = ipaddress.ip_network(destination_cidr)
    for tgw_vpc_att in tgw_vpc_atts:
        tgw_vpc_routes = tgw_vpc_route_repo.get_all_by_tgw_att_id(tgw_vpc_att.id)

        for tgw_vpc_route in tgw_vpc_routes:
            if ipaddress.ip_network(tgw_vpc_route.destination).overlaps(
                destination_cidr_ip
            ):
                return True

    tgw_peering_atts = tgw_peering_att_repo.get_all(tgw_id)

    for tgw_peering_att in tgw_peering_atts:
        tgw_peering_routes = tgw_peering_route_repo.get_all(tgw_peering_att.id)

        for tgw_peering_route in tgw_peering_routes:
            if ipaddress.ip_network(tgw_peering_route.destination_cidr).overlaps(
                destination_cidr_ip
            ):
                return True

    return False
