from fastapi import FastAPI


from transit.api.new_routes.main import api_router


app = FastAPI()

app.include_router(api_router)
