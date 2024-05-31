import openstack
from oslo_config import cfg

CONF = cfg.CONF


class OpenStackAuth:
    """
    Return openstack client object

    """

    @staticmethod
    def get_connection():

        auth_url = CONF.transit.auth_url
        project_name = CONF.transit.project_name
        username = CONF.transit.username
        password = CONF.transit.password
        region_name = CONF.transit.region_name
        project_domain_name = CONF.transit.project_domain_name
        user_domain_name = CONF.transit.user_domain_name

        return openstack.connect(
            AUTH_URL=auth_url,
            PROJECT_NAME=project_name,
            USERNAME=username,
            PASSWORD=password,
            REGION_NAME=region_name,
            PROJECT_DOMAIN_NAME=project_domain_name,
            USER_DOMAIN_NAME=user_domain_name,
        )
