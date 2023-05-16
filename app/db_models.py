from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, BigInteger, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(50))


class Result(Base):
    __tablename__ = "results"

    id: Mapped[int] = mapped_column(primary_key=True)
    naziv: Mapped[str] = mapped_column(String(255))
    adresa: Mapped[str] = mapped_column(String(255))
    telefon: Mapped[str] = mapped_column(String(255))
    GodisnjiPrihodi: Mapped[int] = mapped_column(BigInteger)
    Delatnost: Mapped[str] = mapped_column(String(255))
    BrojZaposlenih: Mapped[int] = mapped_column(Integer)
    FinansijskiPZ: Mapped[int] = mapped_column(Integer)
    FinansijskiPK: Mapped[int] = mapped_column(Integer)
    LicniPK: Mapped[int] = mapped_column(Integer)
    MedicinskiPK: Mapped[int] = mapped_column(Integer)
    DeljenjePK: Mapped[int] = mapped_column(Integer)
    EksterneUsluge: Mapped[str] = mapped_column(String(255))
    EnkripcijaPodataka: Mapped[str] = mapped_column(String(255))
    Websajt: Mapped[int] = mapped_column(Integer)
    BrojJavnihURL: Mapped[int] = mapped_column(Integer)
    TehnickeMere: Mapped[str] = mapped_column(String(255))
    PolitikaPrivatnosti: Mapped[int] = mapped_column(Integer)
    PolitikaZadrzavanjaIBrisanja: Mapped[int] = mapped_column(Integer)
    PolitikaIB: Mapped[str] = mapped_column(String(255))
    BezbednosniTestovi: Mapped[int] = mapped_column(Integer)
    PlanReagovanjaNaIncident: Mapped[int] = mapped_column(Integer)
    PlanOporavka: Mapped[int] = mapped_column(Integer)
    KreiranjeRezervnihKopija: Mapped[int] = mapped_column(Integer)
    BezbednoSkladistenjePodataka: Mapped[int] = mapped_column(Integer)
    ObukaIB: Mapped[int] = mapped_column(Integer)
    ZakonPOLPP: Mapped[int] = mapped_column(Integer)
    pcidss: Mapped[int] = mapped_column(Integer)
    iso27001: Mapped[int] = mapped_column(Integer)
    ZeljeniIznosNaknade: Mapped[int] = mapped_column(Integer)
    BrojIncidenata: Mapped[int] = mapped_column(Integer)
