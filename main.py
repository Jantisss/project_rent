from typing import Union
from fastapi import FastAPI,HTTPException
from models import *
from requests import *
from fastapi.middleware.cors import CORSMiddleware




engine = create_engine("postgresql://postgres:1234@localhost:5432/postgres")
SQLModel.metadata.create_all(engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
def create_new_order(order: OrderCreate):
    # Установка дат по умолчанию, если они не указаны
    if order.date_s is None:
        order.date_s = datetime.today()
    if order.date_e is None:
        order.date_e = datetime.today() + timedelta(days=1)
    
    # Ваша логика создания заказа
    try:
        create_order(
            car_id=order.car_id,
            user_tel=order.user_tel,
            cost_day=order.cost_day,
            date_s=order.date_s,
            date_e=order.date_e,
            office_id=order.office_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": f"Order created for car ID {order.car_id}, user ID {order.user_tel}."}


