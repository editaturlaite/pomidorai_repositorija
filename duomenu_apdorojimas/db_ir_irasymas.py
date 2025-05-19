from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import os

Bazine_klase = declarative_base()

class PomidoraiTrenyravimas(Bazine_klase):
    __tablename__ = 'Pomidoru_lapai_trenyravimo_duomenys'
    id = Column(Integer, primary_key=True)
    kelias = Column(String, unique=True, nullable=False)
    klases_pavadinimas = Column(String, nullable=False)

class PomidoraiValidacija(Bazine_klase):
    __tablename__ = 'Pomidoru_lapai_validacijos_duomenys'
    id = Column(Integer, primary_key=True)
    kelias = Column(String, unique=True, nullable=False)
    klases_pavadinimas = Column(String, nullable=False)

class PomidoraiTestas(Bazine_klase):
    __tablename__ = 'Pomidoru_lapai_testo_duomenys'
    id = Column(Integer, primary_key=True)
    kelias = Column(String, unique=True, nullable=False)
    klases_pavadinimas = Column(String, nullable=False)


def sukurti_sesija():
    rysys_su_baze = create_engine('sqlite:///duomenu_baze/pomidoru_lapai.db')
    Session = sessionmaker(bind=rysys_su_baze)
    sesija = Session()
    return rysys_su_baze, Session, sesija


# ----------------------------------------------------------------------------------------------------

def irasyti_trenyravimo_paveikslelius(sesija, trenyravimo_kelias):

    for klases_pavadinimas in os.listdir(trenyravimo_kelias):
        klases_kelias = os.path.join(trenyravimo_kelias,klases_pavadinimas)

        if os.path.isdir(klases_kelias):
            for paveikslelio_pavadinimas in os.listdir(klases_kelias):
                paveikslelio_kelias = os.path.join(klases_kelias,paveikslelio_pavadinimas)

                egzistuoja = sesija.query(PomidoraiTrenyravimas).filter_by(kelias=paveikslelio_kelias).first()

                if not egzistuoja:

                    naujas_irasas = PomidoraiTrenyravimas(kelias = paveikslelio_kelias, klases_pavadinimas = klases_pavadinimas)

                    sesija.add(naujas_irasas)

    sesija.commit()

    print("Irasyti trenyravimo paveiksleiai")


def irasyti_validacijos_paveikslelius(sesija, validacijos_kelias):

    for klases_pavadinimas in os.listdir(validacijos_kelias):
        klases_kelias = os.path.join(validacijos_kelias,klases_pavadinimas)

        if os.path.isdir(klases_kelias):
            for paveikslelio_pavadinimas in os.listdir(klases_kelias):
                paveikslelio_kelias = os.path.join(klases_kelias,paveikslelio_pavadinimas)

                egzistuoja = sesija.query(PomidoraiValidacija).filter_by(kelias=paveikslelio_kelias).first()

                if not egzistuoja:

                    naujas_irasas = PomidoraiValidacija(kelias = paveikslelio_kelias, klases_pavadinimas = klases_pavadinimas)

                    sesija.add(naujas_irasas)

    sesija.commit()

    print("Irasyti validacijos paveiksleiai")


def irasyti_testo_paveikslelius(sesija, testo_kelias):

    for klases_pavadinimas in os.listdir(testo_kelias):
        klases_kelias = os.path.join(testo_kelias,klases_pavadinimas)

        if os.path.isdir(klases_kelias):
            for paveikslelio_pavadinimas in os.listdir(klases_kelias):
                paveikslelio_kelias = os.path.join(klases_kelias,paveikslelio_pavadinimas)

                egzistuoja = sesija.query(PomidoraiTestas).filter_by(kelias=paveikslelio_kelias).first()

                if not egzistuoja:

                    naujas_irasas = PomidoraiTestas(kelias = paveikslelio_kelias, klases_pavadinimas = klases_pavadinimas)

                    sesija.add(naujas_irasas)

    sesija.commit()

    print("Irasyti testo paveiksleiai")



# --------------------------------------------------------------------------------------------------------
# HSV

class PomidoraiTrenyravimasHSV(Bazine_klase):
    __tablename__ = 'Pomidoru_lapai_trenyravimo_hsv'
    id = Column(Integer,primary_key = True)
    kelias = Column(String, unique=True, nullable=False)  
    klases_pavadinimas = Column(String, nullable=False)

class PomidoraiValidacijaHSV(Bazine_klase):
    __tablename__ = 'Pomidoru_lapai_validacijos_hsv'
    id = Column(Integer,primary_key = True)
    kelias = Column(String, unique=True, nullable=False)  
    klases_pavadinimas = Column(String, nullable=False)

class PomidoraiTestasHSV(Bazine_klase):
    __tablename__ = 'Pomidoru_lapai_testo_hsv'
    id = Column(Integer,primary_key = True)
    kelias = Column(String, unique=True, nullable=False)  
    klases_pavadinimas = Column(String, nullable=False)


def irasyti_trenyravimo_paveikslelius_HSV(sesija, trenyravimo_kelias):
    for klases_pavadinimas in os.listdir(trenyravimo_kelias):
        klases_kelias = os.path.join(trenyravimo_kelias,klases_pavadinimas)
        if os.path.isdir(klases_kelias):
            for paveikslelio_pavadinimas in os.listdir(klases_kelias):
                paveikslelio_kelias = os.path.join(klases_kelias,paveikslelio_pavadinimas)
                egzistuoja = sesija.query(PomidoraiTrenyravimasHSV).filter_by(kelias=paveikslelio_kelias).first()
                if not egzistuoja:
                    naujas_irasas = PomidoraiTrenyravimasHSV(kelias = paveikslelio_kelias, klases_pavadinimas = klases_pavadinimas)
                    sesija.add(naujas_irasas)
    sesija.commit()
    print("Irasyti treniravimo HSV paveiksleiai")

def irasyti_validacijos_paveikslelius_HSV(sesija, validacijos_kelias):
    for klases_pavadinimas in os.listdir(validacijos_kelias):
        klases_kelias = os.path.join(validacijos_kelias,klases_pavadinimas)
        if os.path.isdir(klases_kelias):
            for paveikslelio_pavadinimas in os.listdir(klases_kelias):
                paveikslelio_kelias = os.path.join(klases_kelias,paveikslelio_pavadinimas)
                egzistuoja = sesija.query(PomidoraiValidacijaHSV).filter_by(kelias=paveikslelio_kelias).first()
                if not egzistuoja:
                    naujas_irasas = PomidoraiValidacijaHSV(kelias = paveikslelio_kelias, klases_pavadinimas = klases_pavadinimas)
                    sesija.add(naujas_irasas)
    sesija.commit()
    print("Irasyti validacijos HSV paveiksleiai")

def irasyti_testo_paveikslelius_HSV(sesija, testo_kelias):
    for klases_pavadinimas in os.listdir(testo_kelias):
        klases_kelias = os.path.join(testo_kelias,klases_pavadinimas)
        if os.path.isdir(klases_kelias):
            for paveikslelio_pavadinimas in os.listdir(klases_kelias):
                paveikslelio_kelias = os.path.join(klases_kelias,paveikslelio_pavadinimas)
                egzistuoja = sesija.query(PomidoraiTestasHSV).filter_by(kelias=paveikslelio_kelias).first()
                if not egzistuoja:
                    naujas_irasas = PomidoraiTestasHSV(kelias = paveikslelio_kelias, klases_pavadinimas = klases_pavadinimas)
                    sesija.add(naujas_irasas)
    sesija.commit()
    print("Irasyti testo HSV paveiksleiai")


