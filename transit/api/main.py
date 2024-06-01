import uvicorn

from oslo_config import cfg


def main():
    uvicorn.run(
        "transit.api.app:app",
        reload=cfg.CONF.api_settings.reload,
        host=cfg.CONF.api_settings.bind_host,
        port=cfg.CONF.api_settings.bind_port,
        log_level=3,
    )
