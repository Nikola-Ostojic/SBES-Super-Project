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
    cursor.execute('''
        create TABLE if not exists Results(
            Naziv varchar(255),
            Adresa varchar(255),
            Telefon varchar(255),
            GodisnjiPrihodi int,
            Delatnost int,
            BrojZaposlenih int,
            FinansijskiPZ int,
            FinansijskiPK int,
            LicniPK int,
            MedicinskiPK int,
            DeljenjePK int,
            EksterneUsluge int,
            EnkripcijaPodataka int,
            Websajt int,
            BrojJavnihURL int,
            TehnickeMere int,
            PolitikaPrivatnosti int,
            PolitikaZadrzavanjaIBrisanja int,
            PolitikaIB int,
            BezbednosniTestovi int,
            PlanReagovanjaNaIncident int,
            PlanOporavka int,
            KreiranjeRezervnihKopija int,
            BezbednoSkladistenjePodataka int,
            ObukaIB int,
            ZakonPOLPP int,
            PCIDSS int,
            ISO27001 int,
            ZeljeniIznosNaknade int,
            BrojIncidenata int
        )
    ''')

def insert_row(database, row_data):
    values = ""

    for column in row_data.keys():
        if row_data.get(column):
            if isinstance(row_data[column], int):
                values += row_data[column]
            else:
                values += "'" + row_data[column] + "'"
            values += ','        

    values = values[:-1]

    print(values, flush=True)

    cursor = database.cursor()

    statement = "INSERT INTO Results VALUES ({})".format(values)

    cursor.execute(statement)
