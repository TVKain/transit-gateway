from taskflow import engines

from transit.controller.worker.flows.transit_gateway import TransitGatewayFlow


class ControllerWorker:
    def __init__(self):
        pass

    def create_transit_gateway(self, transit_gateway):
        flow = TransitGatewayFlow.get_transit_gateway_create_flow()

        store = {
            "transit_gateway_id": transit_gateway["id"],
            "vytransit_name": transit_gateway["name"],
        }

        self._run_flow(flow=flow, store=store)

    def _run_flow(self, flow, store):
        e = engines.load(
            flow, excutor="threaded", engine="parallel", max_workers=1, store=store
        )
        e.run()
