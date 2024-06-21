import os

import json

import time

from dotenv import load_dotenv

import requests

import logging

load_dotenv()


class VyTransitDriver:
    def __init__(
        self, management_ip: str, timeout: int = 120, polling_interval: int = 5
    ):
        self._base_path = f"http://{management_ip}:{os.getenv('VYTRANSIT_API_PORT')}"
        self._timeout = timeout
        self._polling_interval = polling_interval

    def health_check(self):
        """Polling vytransit health check endpoint to check if vytransit is up and running"""
        current_trial = 0
        end_time = time.time() + self._timeout
        while time.time() < end_time:
            try:
                response = requests.get(
                    f"{self._base_path}/health/", timeout=self._polling_interval
                )
                if response.status_code == 200:
                    return True
            except requests.exceptions.RequestException as e:
                logging.info(f"Polling health check: {current_trial}")
            time.sleep(self._polling_interval)

            current_trial += 1
        return False

    def add_vpc_route(self, vpc_cidr: str, vpc_net_ip: str):

        logging.info(f"Adding route to VPC CIDR {vpc_cidr} next hop {vpc_net_ip}")

        try:
            response = requests.post(
                url=f"{self._base_path}/routings/",
                data=json.dumps({"destination": vpc_cidr, "next_hop": vpc_net_ip}),
                timeout=self._timeout,
                headers={
                    "accept": "application/json",
                    "Content-Type": "application/json",
                },
            )
            response.raise_for_status()

            logging.info(f"Route added to VPC CIDR {vpc_cidr}")

        except requests.exceptions.RequestException as e:
            logging.error(f"Error adding route: {e}")
            raise Exception("Error adding route") from e

    def remove_vpc_route(self, vpc_cidr: str, vpc_net_ip: str):
        try:
            response = requests.delete(
                f"{self._base_path}/routings/",
                data=json.dumps({"destination": vpc_cidr, "next_hop": vpc_net_ip}),
                timeout=self._timeout,
                headers={
                    "accept": "application/json",
                    "Content-Type": "application/json",
                },
            )
            response.raise_for_status()

            logging.info(f"Route removed from VPC CIDR {vpc_cidr}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error removing route: {e}")
            raise Exception("Error removing route") from e
