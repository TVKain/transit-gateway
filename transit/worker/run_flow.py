from taskflow import engines


def run_flow(flow, store):
    e = engines.load(
        flow, excutor="threaded", engine="parallel", max_workers=2, store=store
    )
    e.run()
