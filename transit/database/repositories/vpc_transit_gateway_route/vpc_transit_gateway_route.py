from transit.database.adapter import DBAdapter


from transit.database.models.vpc_transit_gateway_route import (
    VPCTransitGatewayRouteModel,
)


class VPCTransitGatewayRouteRepository:
    def __init__(self):
        self._db_adapter = DBAdapter()

    def get(
        self,
        ident: str,
    ):
        try:
            with self._db_adapter.get_session() as session:
                vpc_tgw_route = (
                    session.query(VPCTransitGatewayRouteModel)
                    .filter_by(id=ident)
                    .first()
                )

                return VPCTransitGatewayRouteModel.model_validate(vpc_tgw_route)
        except Exception as e:
            raise e

    def create(
        self,
        vpc_id: str,
        destination_cidr: str,
        transit_gateway_vpc_attachment_id: str,
        status: str = "PENDING",
    ):
        try:
            with self._db_adapter.get_session() as session:
                vpc_tgw_route = VPCTransitGatewayRouteModel(
                    vpc_id=vpc_id,
                    destination=destination_cidr,
                    target=transit_gateway_vpc_attachment_id,
                    status=status,
                )

                session.add(vpc_tgw_route)
                session.commit()

                return VPCTransitGatewayRouteModel.model_validate(vpc_tgw_route)
        except Exception as e:
            raise e

    def get_by_vpc_id(self, vpc_id: str):
        try:
            with self._db_adapter.get_session() as session:
                if not vpc_id:
                    raise Exception("Invalid vpc_id")

                vpc_tgw_route = (
                    session.query(VPCTransitGatewayRouteModel)
                    .filter_by(vpc_id=vpc_id)
                    .all()
                )

                return [
                    VPCTransitGatewayRouteModel.model_validate(route)
                    for route in vpc_tgw_route
                ]
        except Exception as e:
            raise e

    def update_status(self, ident: str, status: str):
        try:
            with self._db_adapter.get_session() as session:
                vpc_tgw_route = (
                    session.query(VPCTransitGatewayRouteModel)
                    .filter_by(id=ident)
                    .first()
                )

                vpc_tgw_route.status = status

                session.commit()
        except Exception as e:
            raise e

    def delete(self, ident: str):
        try:
            with self._db_adapter.get_session() as session:
                vpc_tgw_route = (
                    session.query(VPCTransitGatewayRouteModel)
                    .filter_by(id=ident)
                    .first()
                )

                session.delete(vpc_tgw_route)
                session.commit()
        except Exception as e:
            raise e
