import mysql.connector
from logging import error
import traceback
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from db_models import User, Base
import os


def get_db_engine():
    engine = create_engine('mysql+mysqlconnector://{}:{}@db:3306/{}'
                           .format(os.getenv('MYSQL_USER'),
                                   os.getenv('MYSQL_PASSWORD'),
                                   os.getenv('MYSQL_DATABASE')))
    return engine


def init_tables(engine):
    Base.metadata.create_all(engine)


# DEPRICATED - ovde je samo zbog inserta
def get_database_instance():
    try:
        database = mysql.connector.connect(
                host="db",
                user="root",
                password="root",
                port="3306",
                database="sbesproject"
                )

        return database
    except Exception as e:
        traceback.print_exception(e)
        return None


# DEPRICATED - ovo mozda ni ne radi jer sam promenio
# pcidss i iso27001 u mala slova treba testirati
def insert_row(database, row_data):
    values = ""
    br = 0
    for column in row_data.keys():
        br += 1
        if row_data.get(column) is not None:
            print('printanje: ', row_data[column], flush=True)
            if isinstance(row_data[column], int):
                values += str(row_data[column])
            else:
                values += "'" + row_data[column] + "'"
            values += ','

    values = values[:-1]

    cursor = database.cursor()

    statement = "INSERT INTO Results VALUES ({})".format(values)

    cursor.execute(statement)
    database.commit()
