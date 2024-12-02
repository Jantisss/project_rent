from typing import Union
from fastapi import FastAPI
from models import *
from selects import *
from pydantic import BaseModel

from flask import Flask, render_template

appf = Flask(__name__)

@appf.route('/')
def home():
    return render_template('index.html')


engine = create_engine("postgresql://postgres:1234@localhost:5432/postgres")
SQLModel.metadata.create_all(engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to the Car Rental API!"}


@app.get("/selects/cars")
def read_cars():
    return select_cars()


@app.get("/selects/orders")
def read_orders():
    return select_orders()


@app.get("/selects/available_cars")
def read_available_cars():
    return select_available_cars()


@app.get("/selects/available_and_rent_end_cars")
def read_available_and_rent_end_cars():
    return select_available_cars_and_rent_end_cars()


@app.get("/selects/address_pickup")
def read_address_pickup():
    return select_adress_pickup()


@app.post("/bron_rent_car/{car_id}")
def bron_car(car_id: int):
    bron_rent_car(car_id)
    return {"message": f"Car with ID {car_id} has been booked."}


@app.post("/create_order/")
def create_new_order(
    car_id: int,
    user_id: int,
    cost_day: float = 0,
    date_s: Union[datetime, None] = None,
    date_e: Union[datetime, None] = None,
    office_id: int = 1,
):
    if date_s is None:
        date_s = datetime.today()
    if date_e is None:
        date_e = datetime.today() + timedelta(days=1)
    create_order(car_id, user_id, cost_day, date_s, date_e, office_id)
    return {"message": f"Order created for car ID {car_id}, user ID {user_id}."}


if __name__ == "__main__":
    appf.run(debug=True)