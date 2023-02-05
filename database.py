import mysql.connector
from os import getenv

def get_database_instance():    
    database = mysql.connector.connect(
    host="localhost",
    user="Aleksej",
    password="",
    database="sbesproject"
    )

    return database

def init_database(database):
    cursor = database.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Results (Name VARCHAR(255), Score INTEGER)")
