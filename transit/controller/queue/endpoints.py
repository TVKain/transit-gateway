from oslo_config import cfg

from transit.controller.worker.worker import ControllerWorker


class Endpoints:
    def __init__(self):
        self.worker = ControllerWorker()

    def create_transit_gateway(self, context, transit_gateway):

        self.worker.create_transit_gateway(transit_gateway=transit_gateway)
