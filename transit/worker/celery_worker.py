import os

from dotenv import load_dotenv

from celery import Celery

load_dotenv()

app = Celery("transit", broker=os.getenv("CELERY_BROKER_URL"), backend="rpc://")
app.autodiscover_tasks(["transit.worker.transit_gateway"])
app.autodiscover_tasks(["transit.worker.transit_gateway_vpc_attachment"])
app.autodiscover_tasks(["transit.worker.transit_gateway_vpc_route"])
app.autodiscover_tasks(["transit.worker.vpc_transit_gateway_route"])
app.autodiscover_tasks(["transit.worker.transit_gateway_peering_attachment"])
app.autodiscover_tasks(["transit.worker.transit_gateway_peering_route"])
