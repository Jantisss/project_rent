from models import *

def run_script(dels = True):
    try:
        # Подключиться к существующей базе данных
        connection = connect(user="postgres",
                                    # пароль, который указали при установке PostgreSQL
                                    password="1234",
                                    host="127.0.0.1",
                                    port="5432"
                                    )

        # Создайте курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        # SQL-запрос для создания новой таблицы
        # Выполнение команды: это создает новую таблицу
        if (dels):
            cursor.execute(open("Script-4.sql", "r").read())
        connection.commit()
        print("Скрипт успешно выполнен в PostgreSQL")

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")


# run_script()
