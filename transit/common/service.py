"""
Purpose: 
    This module provides prepare_configuration function for all services to use

"""

from oslo_config import cfg

from transit.common import config
from transit.common import rpc


def prepare_configuration(argv):
    """
    Set up the global configuration file.

    This function initializes the global configuration using the provided arguments.
    It calls the `config.init()` function with the arguments, excluding the first
    argument in the list, which is typically the script name.

    Initialize rpc modules

    Args:
        argv (List[str]): A list of arguments to pass to the `config.init()` function.
                          The first element of the list is usually the script name
                          and is ignored.

    Returns:
        None
    """
    print(argv)

    argv = argv or []

    config.init(argv[1:])

    print("Configuration loaded")

    for k, v in cfg.CONF.items():

        if isinstance(v, cfg.ConfigOpts.GroupAttr):
            print(f"[{k}]")
            for i, j in v.items():
                print(f"{i} = {j}")
        else:
            print(f"{k} = {v}")

        print()


def prepare_rpc():
    rpc.init()
    print("RPC module initialized")
