from enum import unique
from typing import List
from typing import Optional
from jinja2.nodes import For
from sqlalchemy import ForeignKey
from sqlalchemy import String, BigInteger, Integer, Boolean, Float
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    Id: Mapped[int] = mapped_column(primary_key=True)
    Username: Mapped[str] = mapped_column(String(30), unique=True)
    Password: Mapped[str] = mapped_column(String(50))

class Result(Base):
    __tablename__ = "results"
    __table_args__ = {'mysql_charset': 'utf8mb4'}

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
    Factor = relationship("Factor", backref='result', uselist=False)
    SelectedItem = relationship("SelectedItem", back_populates="Result")

class ResultCritical(Base):
    __tablename__ = "resultsCritical"
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    Id: Mapped[int] = mapped_column(primary_key=True)
    Naziv: Mapped[str] = mapped_column(String(255))
    Adresa: Mapped[str] = mapped_column(String(255))
    Telefon: Mapped[str] = mapped_column(String(255))
    GodisnjiPrihodi: Mapped[int] = mapped_column(BigInteger)
    BrojZaposlenih: Mapped[int] = mapped_column(Integer)
    PristupPoUlogama: Mapped[int] = mapped_column(Integer)
    PracenjeAktivZapos: Mapped[int] = mapped_column(Integer)
    EdukacijaZapos: Mapped[int] = mapped_column(Integer)
    NDAZakon: Mapped[int] = mapped_column(Integer)
    ObukeZapos: Mapped[int] = mapped_column(Integer)
 
    KlasifPodataka: Mapped[int] = mapped_column(Integer)
    DozvoljeniNosaci: Mapped[int] = mapped_column(Integer)
    PrivatniNosaci: Mapped[int] = mapped_column(Integer)
    SifrovanjePodat: Mapped[int] = mapped_column(Integer)
    EnkriptovanaBaza: Mapped[int] = mapped_column(Integer)
    EndToEndEnkrip: Mapped[int] = mapped_column(Integer)
    VPN: Mapped[int] = mapped_column(Integer)

    KreiranjeIUkidanjeNaloga: Mapped[int] = mapped_column(Integer)
    LozinkaZaPristup: Mapped[int] = mapped_column(Integer)
    DvofaktorskaAutent: Mapped[int] = mapped_column(Integer)
    DigitalniSert: Mapped[int] = mapped_column(Integer)
    PravilaSifri: Mapped[int] = mapped_column(Integer)
    InicijalnaSifra: Mapped[int] = mapped_column(Integer)
    PromenaNalogaDS: Mapped[int] = mapped_column(Integer)
    PristupNaZahtev: Mapped[int] = mapped_column(Integer)
    NajnizePrivil: Mapped[int] = mapped_column(Integer)
    InstalacijaDodatnogSoft: Mapped[int] = mapped_column(Integer)

    LokalizovaniServ: Mapped[int] = mapped_column(Integer)
    OgranicenPristupServ: Mapped[int] = mapped_column(Integer)
    ZasticeniServ: Mapped[int] = mapped_column(Integer)
    FizickoZasticeniServ: Mapped[int] = mapped_column(Integer)
    ElektromegnetnoZrac: Mapped[int] = mapped_column(Integer)
    UPS: Mapped[int] = mapped_column(Integer)

    Sesija: Mapped[int] = mapped_column(Integer)
    AzuriranjeSoft: Mapped[int] = mapped_column(Integer)
    AntivirusFirewall: Mapped[int] = mapped_column(Integer)
    BlokiraniPortovi: Mapped[int] = mapped_column(Integer)
    DMZ: Mapped[int] = mapped_column(Integer)
    BastionServeri: Mapped[int] = mapped_column(Integer)
    IDSIPS: Mapped[int] = mapped_column(Integer)
    
    RezervneKopije: Mapped[int] = mapped_column(Integer)
    DnevneKopije: Mapped[int] = mapped_column(Integer)
    SedmicneKopije: Mapped[int] = mapped_column(Integer)
    MesecneKopije: Mapped[int] = mapped_column(Integer)
    GodisnjeKopije: Mapped[int] = mapped_column(Integer)

    LogAktivnostiKoris: Mapped[int] = mapped_column(Integer)
    CuvanjeLogova: Mapped[int] = mapped_column(Integer)
    PenetrationTesting: Mapped[int] = mapped_column(Integer)
    ProcUpravljanjemIncid: Mapped[int] = mapped_column(Integer)
    ProcTestiranja: Mapped[int] = mapped_column(Integer)
    AzuriranjeTestiranja: Mapped[int] = mapped_column(Integer)
    ProcZaOporavak: Mapped[int] = mapped_column(Integer)
    PrijavaCERTu: Mapped[int] = mapped_column(Integer)

    ZeljeniIznosNaknade: Mapped[int] = mapped_column(Integer)
    BrojIncidenata: Mapped[int] = mapped_column(Integer)
    Factor = relationship("Factor", backref='result', uselist=False)
    SelectedItem = relationship("SelectedItem", back_populates="Result")


class Factor(Base):
    __tablename__ = "factors"
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    Id: Mapped[int] = mapped_column(primary_key=True)
    BaznaPremija: Mapped[int] = mapped_column(BigInteger)
    Factor1: Mapped[float] = mapped_column(Float)
    Factor2: Mapped[float] = mapped_column(Float)
    Factor3: Mapped[float] = mapped_column(Float)
    Factor4: Mapped[float] = mapped_column(Float)
    Factor5: Mapped[float] = mapped_column(Float)
    Factor6: Mapped[float] = mapped_column(Float)
    Factor7: Mapped[float] = mapped_column(Float)
    Factor8: Mapped[float] = mapped_column(Float)
    ResultId: Mapped[Result] = mapped_column(ForeignKey("results.Id"), unique=True)
    Result = relationship("Result", back_populates="Factor")


class CheckedItem(Base):
    __tablename__ = "checked_items"
    __table_args__ = {'mysql_charset': 'utf8mb4'}
    Id: Mapped[str] = mapped_column(String(255), primary_key=True)
    Text: Mapped[String] = mapped_column(String(255))
    SelectedItem = relationship("SelectedItem", back_populates="CheckedItem")


class SelectedItem(Base):
    __tablename__ = "selected_items"
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    Id: Mapped[int] = mapped_column(primary_key=True)
    CheckedItemId: Mapped[str] = mapped_column(ForeignKey("checked_items.Id"))
    CheckedItem = relationship("CheckedItem", back_populates="SelectedItem")
    ResultId: Mapped[int] = mapped_column(ForeignKey("results.Id"))
    Result = relationship("Result", back_populates="SelectedItem")
