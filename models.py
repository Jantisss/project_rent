from typing import Optional
from datetime import datetime, date, timedelta
from sqlmodel import Field, SQLModel, create_engine, Session
from sqlalchemy import Column, String, ForeignKey
from psycopg2 import Error, connect
from pydantic import BaseModel


class users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tel_number: str | None = Field(default=None,unique=True)

class cars(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    vin_code: str
    cost_day : int
    car_reg_plate: str
    date_available: date
    status_id: int = Field(foreign_key="status_table_car.status_id")
    models_id: int = Field(sa_column=Column("model_id", ForeignKey("models.id"))) 

class orders(SQLModel, table=True):
    orders_id: Optional[int] = Field(default=None, primary_key=True)
    car_id: int = Field(foreign_key="cars.id")
    sum: int
    user_id: int = Field(foreign_key="users.id")
    orders_status_id: int = Field(foreign_key="status_table_order.status_id")
    office_id: int = Field(foreign_key="office.id")
    date_time_reg: datetime
    date_start: date
    date_end: date

class status_table_car(SQLModel, table=True):
    status_id: Optional[int] = Field(default=None, primary_key=True)
    status_name: str

class status_table_order(SQLModel, table=True):
    status_id: Optional[int] = Field(default=None, primary_key=True)
    status_name: str
    
class models(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name_models: str
    brands_id: int = Field(foreign_key="brands.id")

class brands(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

class status_table_office(SQLModel, table=True):
    status_id: Optional[int] = Field(default=None, primary_key=True)
    status_name: str

class office(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    office_status_id: int = Field(default=None,foreign_key="status_table_office.status_id")
    index: int  # test
    name : str
    adress: str    

class OrderCreate(BaseModel):
    car_id: int
    user_id: int
    cost_day: float = 0
    date_s: Optional[date] = None
    date_e: Optional[date] = None
    office_id: int = 1

