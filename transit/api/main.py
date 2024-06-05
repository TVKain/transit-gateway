import sys

import uvicorn

from oslo_config import cfg

from transit.common import service


def main():
    service.prepare_configuration(sys.argv)
    service.prepare_rpc()

    uvicorn.run(
        "transit.api.app:app",
        reload=cfg.CONF.api_settings.reload,
        host=cfg.CONF.api_settings.bind_host,
        port=cfg.CONF.api_settings.bind_port,
        log_level=3,
    )
