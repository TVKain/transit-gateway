import sys

from transit.common import service


service.prepare_configuration(sys.argv)
service.prepare_rpc()
