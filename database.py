import mysql.connector
from os import getenv

def get_database_instance():    
    database = mysql.connector.connect(
    host="localhost",
    user="root",
    password="dragan15",
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
            Delatnost varchar(255),
            BrojZaposlenih int,
            FinansijskiPZ int,
            FinansijskiPK int,
            LicniPK int,
            MedicinskiPK int,
            DeljenjePK int,
            EksterneUsluge varchar(255),
            EnkripcijaPodataka varchar(255),
            Websajt int,
            BrojJavnihURL int,
            TehnickeMere varchar(255),
            PolitikaPrivatnosti int,
            PolitikaZadrzavanjaIBrisanja int,
            PolitikaIB varchar(255),
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
    br = 0
    for column in row_data.keys():
        br += 1
        if row_data.get(column) != None:
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