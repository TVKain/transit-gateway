import oslo_messaging as messaging

import transit.common.constants.rpc as rpc_consts

from transit.common import rpc

from transit.database.repositories.transit_gateway import TransitGatewayRepository


class TransitGatewayController:

    def __init__(self):
        self.transit_gateway_repository = TransitGatewayRepository()

        self.target = messaging.Target(
            topic=rpc_consts.TOPIC,
        )

        self.rpc_client = rpc.get_client(self.target)

    def create(self, **kwargs):
        # Create database entry
        transit_gateway = self.transit_gateway_repository.create(**kwargs)

        # Prepare payload
        payload = {"transit_gateway": transit_gateway}
        # Fire and forget
        self.rpc_client.cast({}, "create_transit_gateway", **payload)

        return transit_gateway

    def get(self, uuid):
        transit_gateway = self.transit_gateway_repository.get(ident=uuid)

        return transit_gateway

    def get_all(self):
        transit_gateways = self.transit_gateway_repository.get_all()
        return transit_gateways

    def update(self, uuid, **kwargs):
        transit_gateway = self.transit_gateway_repository.update(ident=uuid, **kwargs)

        return transit_gateway
