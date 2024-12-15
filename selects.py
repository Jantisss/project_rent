from datetime import datetime
from sqlmodel import Field, SQLModel, create_engine, Session, select
from sqlalchemy import Column, String, ForeignKey
from models import *

engine = create_engine("postgresql://postgres:1234@localhost:5432/postgres")
SQLModel.metadata.create_all(engine)

# Запрос списка автомобилей
def select_cars():    
    with Session(engine) as session:
        mass_return = []
        # statement = select(cars, models, brands).where(cars.models_id == models.id and models.brands_id == brands.id)
        statement = select(cars, models, brands, status_table_car)\
            .join(models, cars.models_id == models.id)\
            .join(brands, models.brands_id == brands.id)\
            .join(status_table_car, status_table_car.status_id == cars.status_id)
        
        results = session.exec(statement)
        #print(results)
        for car, model, brand, status in results:
            mass_return.append((car.id,car.vin_code, car.car_reg_plate, model.name_models, brand.name, status.status_name, car.cost_day))
        session.close()
        return mass_return

def select_orders():    
    with Session(engine) as session:
        mass_return = []
        # statement = select(cars, models, brands).where(cars.models_id == models.id and models.brands_id == brands.id)
        statement = select(orders)
        
        results = session.exec(statement)
        #print(results)
        for orders_res in results:
            mass_return.append(orders_res)
        session.close()
        return mass_return        

def select_available_cars():    
    with Session(engine) as session:
        mass_return = []
        # statement = select(cars, models, brands).where(cars.models_id == models.id and models.brands_id == brands.id)
        statement = select(cars, models, brands, status_table_car)\
                        .join(status_table_car, status_table_car.status_id == cars.status_id)\
                        .join(models, cars.models_id == models.id)\
                        .join(brands, models.brands_id == brands.id)\
                        .where(status_table_car.status_name == 'Available')
        
        results = session.exec(statement)
        #return (results)
        for car, model, brand, status in results:
            mass_return.append((car.id,car.vin_code, car.car_reg_plate, model.name_models, brand.name, status.status_name))
        session.close()
        return mass_return

def select_available_cars_and_rent_end_cars():    
    with Session(engine) as session:
        mass_return = []
        # statement = select(cars, models, brands).where(cars.models_id == models.id and models.brands_id == brands.id)
        statement = select(cars, models, brands, status_table_car)\
                        .join(status_table_car, status_table_car.status_id == cars.status_id)\
                        .join(models, cars.models_id == models.id)\
                        .join(brands, models.brands_id == brands.id)\
                        .where(status_table_car.status_name == 'Available' or cars.date_available != None)
        
        results = session.exec(statement)
        #return (results)
        for car, model, brand, status in results:
            mass_return.append((car.id,car.vin_code, car.car_reg_plate, model.name_models, brand.name, status.status_name, ' | ',car.date_available))
        session.close()
        return mass_return

def select_adress_pickup():    
    with Session(engine) as session:
        mass_return = []
        # statement = select(cars, models, brands).where(cars.models_id == models.id and models.brands_id == brands.id)
        statement = select(office, status_table_office)\
                        .join(status_table_office)\
                        .where(status_table_office.status_name == 'Work')
        
        results = session.exec(statement)
        #return (results)
        for offices, status in results:
            mass_return.append((offices.id, offices.name, offices.adress, offices.index, status.status_name))
        session.close()
        return mass_return

        

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
            car.status_id = result_status
            session.commit()
            return (car)
        
        session.close()

def create_order(car_id, user_tel, cost_day = 0, 
                 date_s = date.today(), 
                 date_e = date.today() + timedelta(days = 1),
                 office_id = 1):
    
    with Session(engine) as session:
        statement_car = select(cars)\
                        .where(cars.id == car_id)
        
        statement_status = select(status_table_order.status_id)\
                        .where(status_table_order.status_name == 'Pending')
        
        statement_status_car = select(status_table_car.status_id)\
                        .where(status_table_car.status_name == 'Rented')
        
        statement_user = select(users)\
                        .where(users.tel_number == str(user_tel))
        
        
        result_status = session.exec(statement_status).first()
        result_car = session.exec(statement_car).one()
        result_status_car = session.exec(statement_status_car).first()
        result_user = session.exec(statement_user).first()
        
        print("res_user", result_user, )
        if result_user == None:
            create_user(user_tel)
        result_user = session.exec(statement_user).first()
        user_id = result_user.id
        
        

        cost_day = result_car.cost_day if result_car.cost_day else cost_day
        

        order = orders(car_id=car_id, user_id=user_id, 
                       orders_status_id=result_status, 
                       office_id=office_id, date_time_reg=datetime.now(), 
                       date_start = date_s, sum = cost_day*(date_e-date_s).days,
                       date_end = date_e)
        
        result_car.status_id = result_status_car
        
        session.add_all([order, result_car])

        session.commit()
        session.close()

        return True
    
def create_user(user_id):
    
    with Session(engine) as session:
        user = users(tel_number=user_id)
        session.add(user)
        session.commit()
        session.close()

        return True

        
if __name__ == '__main__':
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
    #create_order(5,1,123, date.today(), date.today()+ timedelta(days=5))
    print('-'*20)
    #print(select_orders())
    print('*'*20)
    print(date.today())
    print(create_order(1,'79091234652',123,date.fromisoformat("2024-12-12"),date.fromisoformat("2024-12-15"),1))