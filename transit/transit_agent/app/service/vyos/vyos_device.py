import os

from dotenv import load_dotenv


import pyvyos


load_dotenv()

vy_device = pyvyos.VyDevice(
    hostname=os.getenv("VYOS_HOSTNAME"), apikey=os.getenv("VYOS_API_KEY"), verify=False
)
