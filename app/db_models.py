from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, BigInteger, Integer, Boolean
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
    enc_password: Mapped[str] = mapped_column(String(50))
    salt: Mapped[str] = mapped_column(String(50))


class Result(Base):
    __tablename__ = "results"

    Id: Mapped[int] = mapped_column(primary_key=True)
    Naziv: Mapped[str] = mapped_column(String(255))
    Adresa: Mapped[str] = mapped_column(String(255))
    Telefon: Mapped[str] = mapped_column(String(255))
    GodisnjiPrihodi: Mapped[int] = mapped_column(BigInteger)
    BrojZaposlenih: Mapped[int] = mapped_column(Integer)
    FinansijskiPZ: Mapped[bool] = mapped_column(Boolean)
    FinansijskiPK: Mapped[bool] = mapped_column(Boolean)
    LicniPK: Mapped[bool] = mapped_column(Boolean)
    MedicinskiPK: Mapped[bool] = mapped_column(Boolean)
    DeljenjePK: Mapped[bool] = mapped_column(Boolean)
    Websajt: Mapped[bool] = mapped_column(Boolean)
    BrojJavnihURL: Mapped[int] = mapped_column(Integer)
    PolitikaPrivatnosti: Mapped[bool] = mapped_column(Boolean)
    PolitikaZadrzavanjaIBrisanja: Mapped[bool] = mapped_column(Boolean)
    BezbednosniTestovi: Mapped[bool] = mapped_column(Boolean)
    PlanReagovanjaNaIncident: Mapped[bool] = mapped_column(Boolean)
    PlanOporavka: Mapped[bool] = mapped_column(Boolean)
    KreiranjeRezervnihKopija: Mapped[bool] = mapped_column(Boolean)
    BezbednoSkladistenjePodataka: Mapped[bool] = mapped_column(Boolean)
    ObukaIB: Mapped[bool] = mapped_column(Boolean)
    ZakonPOLPP: Mapped[bool] = mapped_column(Boolean)
    Pcidss: Mapped[bool] = mapped_column(Boolean)
    Iso27001: Mapped[bool] = mapped_column(Boolean)
    ZeljeniIznosNaknade: Mapped[int] = mapped_column(Integer)
    BrojIncidenata: Mapped[int] = mapped_column(Integer)
    Factor = relationship("Factor", back_populates="Result")
    CheckedItem = relationship("CheckedItem", back_populates="Result")


class Factor(Base):
    __tablename__ = "factors"

    Id: Mapped[int] = mapped_column(primary_key=True)
    BaznaPremija: Mapped[int] = mapped_column(BigInteger)
    Factor1: Mapped[int] = mapped_column(Integer)
    Factor2: Mapped[int] = mapped_column(Integer)
    Factor3: Mapped[int] = mapped_column(Integer)
    Factor4: Mapped[int] = mapped_column(Integer)
    Factor5: Mapped[int] = mapped_column(Integer)
    Factor6: Mapped[int] = mapped_column(Integer)
    ResultId: Mapped[Result] = mapped_column(ForeignKey("results.Id"))
    Result = relationship("Result", back_populates="Factor")


class CheckedItem(Base):
    __tablename__ = "checked_items"

    Id: Mapped[int] = mapped_column(primary_key=True)
    Text: Mapped[String] = mapped_column(String(255))
    Weight: Mapped[int] = mapped_column(Integer)
    ResultId: Mapped[Result] = mapped_column(ForeignKey("results.Id"))
    Result = relationship("Result", back_populates="CheckedItem")
