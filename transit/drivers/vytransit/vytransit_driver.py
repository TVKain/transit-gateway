import logging


import os

import json

import time

from dotenv import load_dotenv

import requests

from transit.library import pyvyos

load_dotenv()


class VyTransitDriver:
    def __init__(
        self, management_ip: str, timeout: int = 120, polling_interval: int = 5
    ):

        self._timeout = timeout
        self._polling_interval = polling_interval

        self.vy_device = pyvyos.VyDevice(
            hostname=management_ip, apikey="agent-api-key", verify=False
        )

    def health_check(self):
        """Polling vytransit health check endpoint to check if vytransit is up and running"""
        current_trial = 0
        end_time = time.time() + self._timeout
        while time.time() < end_time:

            response = self.vy_device.retrieve_show_config()
            if response.status == 200:
                return True

            if response.status == 0:
                logging.info(f"Polling health check: {current_trial}")
            time.sleep(self._polling_interval)

            current_trial += 1
        return False

    def add_vpc_route(self, vpc_cidr: str, vpc_net_ip: str):

        logging.info(f"Adding route to VPC CIDR {vpc_cidr} next hop {vpc_net_ip}")

        try:
            response = self.vy_device.configure_set(
                path=[
                    "protocols",
                    "static",
                    "route",
                    vpc_cidr,
                    "next-hop",
                    vpc_net_ip,
                ]
            )

            logging.info(f"Response: {response}")

            self.vy_device.config_file_save()

            logging.info(f"Route added to VPC CIDR {vpc_cidr}")

        except requests.exceptions.RequestException as e:
            logging.error(f"Error adding route: {e}")
            raise Exception("Error adding route") from e

    def remove_vpc_route(self, vpc_cidr: str, vpc_net_ip: str):

        logging.info(f"Removing route to VPC CIDR {vpc_cidr} next hop {vpc_net_ip}")

        try:
            response = self.vy_device.configure_delete(
                path=[
                    [
                        "protocols",
                        "static",
                        "route",
                        vpc_cidr,
                        "next-hop",
                        vpc_net_ip,
                    ]
                ]
            )

            self.vy_device.config_file_save()

            logging.info(f"Route removed from VPC CIDR {vpc_cidr}")

        except Exception as e:
            logging.error(f"Error removing route: {e}")
            raise Exception("Error removing route") from e

        return response

    def add_tunnel(
        self,
        tunnel_interface_ip: str,
        remote_tunnel_interface_ip: str,
        tun_num: int,
        tun_ip: str,
    ):
        try:
            print(
                f"Adding tunnel from {tunnel_interface_ip} to {remote_tunnel_interface_ip}"
            )

            response = self.vy_device.configure_set(
                path=[
                    [
                        "interfaces",
                        "tunnel",
                        f"tun{tun_num}",
                        "encapsulation",
                        "gre",
                    ],
                    [
                        "interfaces",
                        "tunnel",
                        f"tun{tun_num}",
                        "address",
                        f"{tun_ip}/30",
                    ],
                    [
                        "interfaces",
                        "tunnel",
                        f"tun{tun_num}",
                        "source-address",
                        f"{tunnel_interface_ip}",
                    ],
                    [
                        "interfaces",
                        "tunnel",
                        f"tun{tun_num}",
                        "remote",
                        f"{remote_tunnel_interface_ip}",
                    ],
                ]
            )

            if response.error:
                logging.error(f"Error adding tunnel: {response.error}")
                raise Exception("Error adding tunnel")

            self.vy_device.config_file_save()

            logging.info(f"Response: {response}")

            logging.info(
                f"Tunnel added from {tunnel_interface_ip} to {remote_tunnel_interface_ip}"
            )
        except requests.exceptions.RequestException as e:
            logging.error(f"Error adding tunnel: {e}")
            raise Exception("Error adding tunnel") from e

    def remove_tunnel(self, tun_num: int):
        try:
            response = self.vy_device.configure_delete(
                path=[
                    "interfaces",
                    "tunnel",
                    f"tun{tun_num}",
                ]
            )

            self.vy_device.config_file_save()

            logging.info(f"Response: {response}")

            logging.info(f"Tunnel removed with tun_num {tun_num}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error removing tunnel: {e}")
            raise Exception("Error removing tunnel") from e

    def test(self):
        print(self.vy_device.retrieve_show_config())
