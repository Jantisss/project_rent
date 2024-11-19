from typing import Union
from fastapi import FastAPI
from models import *
from selects import *

engine = create_engine("postgresql://postgres:1234@localhost:5432/postgres")
SQLModel.metadata.create_all(engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/selects/cars")
def read_cars():
    return select_cars()

@app.get("/selects/orders")
def read_orders():
    return select_orders()