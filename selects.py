from datetime import datetime
from sqlmodel import Field, SQLModel, create_engine, Session, select
from sqlalchemy import Column, String, ForeignKey
from models import *

engine = create_engine("postgresql://postgres:1234@localhost:5432/postgres")
SQLModel.metadata.create_all(engine)

# Запрос списка автомобилей
def select_cars():    
    with Session(engine) as session:
        # statement = select(cars, models, brands).where(cars.models_id == models.id and models.brands_id == brands.id)
        statement = select(cars, models, brands).join(models, cars.models_id == models.id).join(brands, models.brands_id == brands.id)
        
        results = session.exec(statement)
        #print(results)
        for car, model, brand in results:
            print(car.id,car.vin_code, car.car_reg_plate, model.name_models, brand.name, car.status_id)

        session.close()

def select_available_cars():    
    with Session(engine) as session:
        # statement = select(cars, models, brands).where(cars.models_id == models.id and models.brands_id == brands.id)
        statement = select(cars, models, brands, status_table_car)\
                        .join(status_table_car, status_table_car.status_id == cars.status_id)\
                        .join(models, cars.models_id == models.id)\
                        .join(brands, models.brands_id == brands.id)\
                        .where(status_table_car.status_name == 'Available')
        
        results = session.exec(statement)
        #print(results)
        for car, model, brand, status in results:
            print(car.id,car.vin_code, car.car_reg_plate, model.name_models, brand.name, status.status_name)

        session.close()

def select_available_cars_and_rent_end_cars():    
    with Session(engine) as session:
        # statement = select(cars, models, brands).where(cars.models_id == models.id and models.brands_id == brands.id)
        statement = select(cars, models, brands, status_table_car)\
                        .join(status_table_car, status_table_car.status_id == cars.status_id)\
                        .join(models, cars.models_id == models.id)\
                        .join(brands, models.brands_id == brands.id)\
                        .where(status_table_car.status_name == 'Available' or cars.date_available != None)
        
        results = session.exec(statement)
        #print(results)
        for car, model, brand, status in results:
            print(car.id,car.vin_code, car.car_reg_plate, model.name_models, brand.name, status.status_name, ' | ',car.date_available)

        session.close()

def select_adress_pickup():    
    with Session(engine) as session:
        # statement = select(cars, models, brands).where(cars.models_id == models.id and models.brands_id == brands.id)
        statement = select(office, status_table_office)\
                        .join(status_table_office)\
                        .where(status_table_office.status_name == 'Work')
        
        results = session.exec(statement)
        #print(results)
        for offic, status in results:
            print(offic, status)

        session.close()

def bron_rent_car(car_id):
    with Session(engine) as session:
        statement_car = select(cars)\
                        .join(status_table_car)\
                        .where(cars.id == car_id)
        
        statement_status = select(status_table_car.status_id)\
                        .where(status_table_car.status_name == 'Rented')
        
        results = session.exec(statement_car)
        result_status = session.exec(statement_status).first()
        
        for car in results:
            print(car)
            car.status_id = result_status
            session.commit()
        
        session.close()

def create_order(car_id, user_id, cost_day = 0, 
                 date_s = date.today(), 
                 date_e = date.today() + timedelta(days = 1),
                 office_id = 1):
    
    with Session(engine) as session:
        statement_car = select(cars.cost_day)\
                        .where(cars.id == car_id)
        
        statement_status = select(status_table_order.status_id)\
                        .where(status_table_order.status_name == 'Pending')
        
        result_status = session.exec(statement_status).first()
        result_car = session.exec(statement_car).first()

        cost_day = result_car if result_car else cost_day

        order = orders(car_id=car_id, user_id=user_id, 
                       orders_status_id=result_status, 
                       office_id=office_id, date_time_reg=datetime.now(), 
                       date_start = date_s, sum = cost_day*(date_e-date_s).days,
                       date_end = date_e)
        
        print(order)

        session.add(order)
        session.commit()
        session.close()

        return True
        

select_cars()
print('-'*20)
select_available_cars()
print('-'*20)
select_available_cars_and_rent_end_cars()
print('-'*20)
select_adress_pickup()
print('-'*20)
bron_rent_car(4)
print('-'*20)
create_order(5,1,123, date.today(), date.today()+ timedelta(days=5))