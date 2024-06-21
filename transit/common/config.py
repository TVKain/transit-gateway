from oslo_config import cfg
from oslo_db import options as db_options
import oslo_messaging as messaging

# Used by the api server
api_opts = [
    cfg.IPOpt("bind_host", default="0.0.0.0", help="The host IP to bind to"),
    cfg.PortOpt("bind_port", default=2607, help="The port to bind to"),
    cfg.BoolOpt(
        "reload",
        default=False,
        help="Enable or disable reload server on change (should only be True in development)",
    ),
]

# Auth information for transit service
transit_opts = [
    cfg.StrOpt(name="auth_url", help="Identity service authentication URL"),
    cfg.StrOpt(name="project_name", help="Project name", default="service"),
    cfg.StrOpt(
        name="username", help="Username for transit service user", default="transit"
    ),
    cfg.StrOpt(name="password", help="Password for transit service user"),
    cfg.StrOpt(name="region_name", help="Region Name for the identity service"),
    cfg.StrOpt(
        name="project_domain_name", help="Project domain name", default="Default"
    ),
    cfg.StrOpt(name="user_domain_name", help="User domain name", default="Default"),
]

# Configuration for vytransit vm
vytransit_opts = [
    cfg.StrOpt(name="flavor_id", help="VyTransit instance flavor id"),
    cfg.StrOpt(name="image_id", help="VyTransit instance image id"),
    cfg.StrOpt(
        name="management_net_id", help="Management network id for VyTransit instance, this should already exist"
    ),
    cfg.StrOpt(
        name="provider_net_id", help="Provider network id for VyTransit instance, this should already exist"
    )
]

# Configuration for controller worker
controller_worker_opts = [
    cfg.IntOpt(
        name="worker_count",
        default=1,
        help="Number of workers for the controller service",
    )
]

# Configuration for DEFAULT
default_opts = [
    cfg.HostnameOpt(name="host", help="The host that the transit service is running on")
]


cfg.CONF.register_opts(api_opts, group="api_settings")
cfg.CONF.register_opts(transit_opts, group="transit")
cfg.CONF.register_opts(vytransit_opts, group="vytransit")
cfg.CONF.register_opts(controller_worker_opts, group="controller_worker")
cfg.CONF.register_opts(default_opts)


messaging.set_transport_defaults(control_exchange="transit")

messaging.TransportURL.parse(cfg.CONF)

_SQL_CONNECTION_DEFAULT = "sqlite://"
db_options.set_defaults(cfg.CONF, connection=_SQL_CONNECTION_DEFAULT)


def init(args, **kwargs):
    """
    Initialize the config from config file
    """
    cfg.CONF(args=args, **kwargs)
