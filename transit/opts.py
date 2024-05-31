"""
Purpose: 
Provides list_opts() function to run with oslo-config-generator
Only use to generate a sample config file 

Simply run 
    oslo-config-generator --namespace transit.config --namespace oslo.db
    
TODO
    Modify the default value of connection in oslo.db
"""

from transit.common.config import api_opts
from transit.common.config import transit_opts
from transit.common.config import vytransit_opts
from transit.common.config import controller_worker_opts
from transit.common.config import default_opts


def list_opts():
    return [
        ("api_settings", api_opts),
        ("transit", transit_opts),
        ("vytransit", vytransit_opts),
        ("controller_worker", controller_worker_opts),
        ("", default_opts),
    ]
