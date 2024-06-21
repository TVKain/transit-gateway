import os

from dotenv import load_dotenv

import openstack


load_dotenv()


class OpenStackAuth:
    """
    Return openstack client object

    """

    @staticmethod
    def get_connection():

        auth_url = os.getenv("AUTH_URL")
        project_name = os.getenv("PROJECT_NAME")
        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")
        region_name = os.getenv("REGION_NAME")
        project_domain_name = os.getenv("PROJECT_DOMAIN_NAME")
        user_domain_name = os.getenv("USER_DOMAIN_NAME")

        return openstack.connect(
            auth_url=auth_url,
            project_name=project_name,
            username=username,
            password=password,
            region_name=region_name,
            project_domain_name=project_domain_name,
            user_domain_name=user_domain_name,
        )
