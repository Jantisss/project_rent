from models import *
from run_script import *

run_script()  # исполнение script-4
# Создаем соединение с базой данных
engine = create_engine("postgresql://postgres:1234@localhost:5432/postgres")
SQLModel.metadata.create_all(engine)

session = Session(engine)

# Добавление данных в таблицы

# Добавляем бренды
brand1 = brands(name="Toyota")
brand2 = brands(name="BMW")
brand3 = brands(name="Mercedes")

session.add_all([brand1, brand2, brand3])
session.commit()
map(session.refresh, [brand1, brand2, brand3])

# print(brand1.id, brand2.id, brand3.id)



# Добавляем модели автомобилей
model1 = models(name_models = "model_1", brands_id=brand1.id)
model2 = models(name_models = "model_2", brands_id=brand2.id)
model3 = models(name_models = "model_3", brands_id=brand3.id)
model4 = models(name_models = "model_4", brands_id=brand1.id)


session.add_all([model1, model2, model3, model4])
session.commit()
map(session.refresh, [model1, model2, model3, model4])

# Добавляем статусы автомобилей
status_car1 = status_table_car(status_name="Available")
status_car2 = status_table_car(status_name="Rented")
status_car3 = status_table_car(status_name="In Service")

session.add_all([status_car1, status_car2, status_car3])
session.commit()
map(session.refresh, [status_car1, status_car2, status_car3])

# Добавляем автомобили
car1 = cars(vin_code="1HGBH41JXMN109186", car_reg_plate="ABC123", status_id=status_car1.status_id, models_id=model1.id)
car2 = cars(vin_code="JH4KA7650MC012345", car_reg_plate="DEF456", status_id=status_car2.status_id, models_id=model2.id)
car3 = cars(vin_code="2HNYD18896H000000", car_reg_plate="GHI789", status_id=status_car3.status_id, models_id=model3.id)
car4 = cars(vin_code="3HNYD12464H000000", car_reg_plate="IHO789", status_id=status_car1.status_id, models_id=model4.id)
car5 = cars(vin_code="4HNYD18246H000000", car_reg_plate="YAI789", status_id=status_car1.status_id, models_id=model1.id)

session.add_all([car1, car2, car3, car4, car5])
session.commit()
map(session.refresh, [car1, car2, car3, car4, car5])


# Добавляем пользователей
user1 = users(tel_number="1234567890")
user2 = users(tel_number="0987654321")
user3 = users(tel_number="5551234567")

session.add_all([user1, user2, user3])
session.commit()
map(session.refresh, [user1, user2, user3])

# Добавляем статусы офисов
status_office_1 = status_table_office(status_name="Work")
status_office_2 = status_table_office(status_name="Building")
status_office_3 = status_table_office(status_name="Closed")

session.add_all([status_office_1, status_office_2, status_office_3])
session.commit()



# Добавляем офисы
office1 = office(name="Downtown", office_status_id=status_office_1.status_id)
office2 = office(name="Airport", office_status_id=status_office_1.status_id)
office3 = office(name="Suburb", office_status_id=status_office_2.status_id)

session.add_all([office1, office2, office3])
session.commit()
map(session.refresh, [office1, office2, office3])


# Добавляем статусы заказов
status_order1 = status_table_order(status_name="Pending")
status_order2 = status_table_order(status_name="Confirmed")
status_order3 = status_table_order(status_name="Cancelled")

session.add_all([status_order1, status_order2, status_order3])
session.commit()
map(session.refresh, [status_order1, status_order2, status_order3])

# Добавляем заказы
order1 = orders(car_id=car1.id, user_id=user1.id, orders_status_id=status_order1.status_id, office_id=office1.id, date_time_reg=datetime.now(), 
                date_start=date.today() + timedelta(days = 5),
                date_end=date.today() + timedelta(days = 7))
order2 = orders(car_id=car2.id, user_id=user2.id, orders_status_id=status_order2.status_id, office_id=office2.id, date_time_reg=datetime.now(), 
                date_start=date.today() + timedelta(days = 5),
                date_end=date.today() + timedelta(days = 7))
order3 = orders(car_id=car3.id, user_id=user3.id, orders_status_id=status_order3.status_id, office_id=office3.id, date_time_reg=datetime.now(), 
                date_start=date.today() + timedelta(days = 5),
                date_end=date.today() + timedelta(days = 7))

car1.date_available = date.today() + timedelta(days = 7)
car1.status_id = status_car2.status_id
car2.date_available = date.today() + timedelta(days = 7)
car2.status_id = status_car2.status_id
car3.date_available = date.today() + timedelta(days = 7)
car3.status_id = status_car2.status_id

session.add_all([order1, order2, order3])
session.commit()
map(session.refresh, [order1, order2, order3])


# Закрываем сессию
session.close()