# Change to fastapi

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.routes.routes import api


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api, prefix="")


# import os

# from flask import Flask

# from dotenv import load_dotenv

# from .routes.routes import api

# from .config.flask_config import FlaskConfig

# current_dir = os.path.dirname(__file__)

# environment = os.environ.get('ENVIRONMENT', 'dev')

# if  environment == 'dev':
#     dotenv_path = os.path.join(current_dir, 'config', '.dev.env')
# elif environment == 'prod':
#     dotenv_path = os.path.join(current_dir, 'config', '.prod.env')
# else:
#     raise ValueError("'ENVIRONMENT' environment variable has an unexpected value.")

# load_dotenv(dotenv_path=dotenv_path)

# flask_config = FlaskConfig(ENV=os.getenv('ENV'),
#                            DEBUG=os.getenv('DEBUG'),
#                            PORT=os.getenv('PORT'),
#                            HOST=os.getenv('HOST'))

# print(flask_config.PORT)

# app = Flask(__name__)

# app.env = flask_config.ENV

# app.register_blueprint(api, url_prefix="/")
