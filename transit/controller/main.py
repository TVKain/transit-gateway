import cotyledon
from cotyledon import oslo_config_glue

from oslo_config import cfg


from transit.controller.queue.consumer import ConsumerService


def main():
    service_manager = cotyledon.ServiceManager()

    service_manager.add(ConsumerService, workers=1, args=(cfg.CONF,))
    oslo_config_glue.setup(service_manager, cfg.CONF, reload_method="mutate")
    service_manager.run()
