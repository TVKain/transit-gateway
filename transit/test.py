from transit.new_worker.transit_gateway.tasks import add

print(add.delay(4, 4).get())
