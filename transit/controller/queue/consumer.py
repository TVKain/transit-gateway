import cotyledon

from oslo_config import cfg
import oslo_messaging as messaging

from transit.common.constants import rpc as rpc_consts
from transit.common import rpc
from transit.controller.queue import endpoints


class ConsumerService(cotyledon.Service):

    def __init__(self, worker_id, conf):
        super().__init__(worker_id)
        self.conf = conf
        self.topic = rpc_consts.TOPIC
        self.server = cfg.CONF.host
        self.endpoints = []

        self.message_listener = None

    def run(self):

        target = messaging.Target(topic=self.topic, server=self.server, fanout=False)
        self.endpoints = [endpoints.Endpoints()]
        self.message_listener = rpc.get_server(
            target,
            self.endpoints,
            executor="threading",
        )
        self.message_listener.start()
        print("Consumer service for controller worker started...")

    def terminate(self):
        if self.message_listener:
            self.message_listener.stop()
            self.message_listener.wait()
        if self.endpoints:
            for e in self.endpoints:
                try:
                    e.worker.executor.shutdown()
                except AttributeError:
                    pass
        super().terminate()
