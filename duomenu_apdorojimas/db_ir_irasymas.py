from sqlalchemy import create_engine, Column, Integer, String,LargeBinary
from sqlalchemy.orm import declarative_base, sessionmaker
import os
import numpy as np

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
# # HSV

# class PomidoraiTrenyravimasHSV(Bazine_klase):
#     __tablename__ = 'Pomidoru_lapai_trenyravimo_hsv'
#     id = Column(Integer,primary_key = True)
#     kelias = Column(String, unique=True, nullable=False)  
#     klases_pavadinimas = Column(String, nullable=False)
#     hsv_duomenys = Column(LargeBinary)

# class PomidoraiValidacijaHSV(Bazine_klase):
#     __tablename__ = 'Pomidoru_lapai_validacijos_hsv'
#     id = Column(Integer,primary_key = True)
#     kelias = Column(String, unique=True, nullable=False)  
#     klases_pavadinimas = Column(String, nullable=False)
#     hsv_duomenys = Column(LargeBinary)

# class PomidoraiTestasHSV(Bazine_klase):
#     __tablename__ = 'Pomidoru_lapai_testo_hsv'
#     id = Column(Integer,primary_key = True)
#     kelias = Column(String, unique=True, nullable=False)  
#     klases_pavadinimas = Column(String, nullable=False)
#     hsv_duomenys = Column(LargeBinary)


# def irasyti_trenyravimo_paveikslelius_HSV(sesija, trenyravimo_kelias):
#     for klases_pavadinimas in os.listdir(trenyravimo_kelias):
#         klases_kelias = os.path.join(trenyravimo_kelias,klases_pavadinimas)
#         if os.path.isdir(klases_kelias):
#             for paveikslelio_pavadinimas in os.listdir(klases_kelias):
#                 paveikslelio_kelias = os.path.join(klases_kelias,paveikslelio_pavadinimas)
#                 egzistuoja = sesija.query(PomidoraiTrenyravimasHSV).filter_by(kelias=paveikslelio_kelias).first()
#                 if not egzistuoja:
#                         hsv = np.load(paveikslelio_kelias)
#                         hsv_bytes = hsv.tobytes()

#                         naujas_irasas = PomidoraiTrenyravimasHSV(kelias=paveikslelio_kelias,klases_pavadinimas=klases_pavadinimas,hsv_duomenys=hsv_bytes)
#                         sesija.add(naujas_irasas)
#     sesija.commit()
#     print("Irasyti treniravimo HSV paveiksleiai")

# def irasyti_validacijos_paveikslelius_HSV(sesija, validacijos_kelias):
#     for klases_pavadinimas in os.listdir(validacijos_kelias):
#         klases_kelias = os.path.join(validacijos_kelias,klases_pavadinimas)
#         if os.path.isdir(klases_kelias):
#             for paveikslelio_pavadinimas in os.listdir(klases_kelias):
#                 paveikslelio_kelias = os.path.join(klases_kelias,paveikslelio_pavadinimas)
#                 egzistuoja = sesija.query(PomidoraiValidacijaHSV).filter_by(kelias=paveikslelio_kelias).first()
#                 if not egzistuoja:
#                         hsv = np.load(paveikslelio_kelias)
#                         hsv_bytes = hsv.tobytes()

#                         naujas_irasas = PomidoraiValidacijaHSV(kelias=paveikslelio_kelias,klases_pavadinimas=klases_pavadinimas,hsv_duomenys=hsv_bytes)
#                         sesija.add(naujas_irasas)
#     sesija.commit()
#     print("Irasyti validacijos HSV paveiksleiai")

# def irasyti_testo_paveikslelius_HSV(sesija, testo_kelias):
#     for klases_pavadinimas in os.listdir(testo_kelias):
#         klases_kelias = os.path.join(testo_kelias,klases_pavadinimas)
#         if os.path.isdir(klases_kelias):
#             for paveikslelio_pavadinimas in os.listdir(klases_kelias):
#                 paveikslelio_kelias = os.path.join(klases_kelias,paveikslelio_pavadinimas)
#                 egzistuoja = sesija.query(PomidoraiTestasHSV).filter_by(kelias=paveikslelio_kelias).first()
#                 if not egzistuoja:
#                         hsv = np.load(paveikslelio_kelias)
#                         hsv_bytes = hsv.tobytes()

#                         naujas_irasas = PomidoraiTestasHSV(kelias=paveikslelio_kelias,klases_pavadinimas=klases_pavadinimas,hsv_duomenys=hsv_bytes)
#                         sesija.add(naujas_irasas)
#     sesija.commit()
#     print("Irasyti testo HSV paveiksleiai")


# -------------------------------------------------------------------------------------------------------

class IkeltaPaveikslelis(Bazine_klase):
    __tablename__ = 'Ikelti_paveiksleliai'
    id = Column(Integer, primary_key=True)
    kelias = Column(String, nullable=False)


def irasyti_ikelta_paveiksleli(sesija, paveikslelio_kelias):
    naujas_paveikslelis = IkeltaPaveikslelis(kelias=paveikslelio_kelias)
    sesija.add(naujas_paveikslelis)
    sesija.commit()

# -----------------------------------------------------------------------------------------------------------


class PatarimasPagalKlase(Bazine_klase):
    __tablename__ = 'Patarimai_klasems'
    id = Column(Integer, primary_key=True)
    klase = Column(String, unique=True, nullable=False)  
    patarimas = Column(String, nullable=False)

def sukurti_patarimus(sesija):
    egzistuoja = sesija.query(PatarimasPagalKlase).first()
    if egzistuoja:
        return  

    patarimai = [
        (
            "Tomato___Late_blight",
            "Vėlyvoji maras yra greitai plintanti grybinė infekcija, kuri ypač suaktyvėja drėgnomis sąlygomis. "
            "Pažeistus lapus ir vaisius rekomenduojama nedelsiant pašalinti ir sunaikinti (nekompostuoti). "
            "Profilaktikai naudokite vario pagrindu pagamintus fungicidus ir laistykite augalus anksti ryte, kad jie spėtų išdžiūti iki vakaro."
        ),
        (
            "Tomato___Septoria_leaf_spot",
            "Septoriozė dažniausiai prasideda nuo apatinių lapų. "
            "Rekomenduojama reguliariai šalinti pažeistus lapus ir užtikrinti gerą oro cirkuliaciją tarp augalų. "
            "Venkite perteklinės drėgmės ant lapų ir naudokite natūralius arba vario pagrindu pagamintus apsauginius preparatus."
        ),
        (
            "Tomato___healthy",
            "Jūsų augalas šiuo metu atrodo sveikas. Toliau rūpinkitės juo atsakingai – reguliariai laistykite rytais, "
            "venkite šlapių lapų vakare, tręškite subalansuotomis trąšomis ir užtikrinkite pakankamą atstumą tarp augalų, kad būtų gera oro cirkuliacija. "
            "Stebėkite augalą ir reaguokite į bet kokius pokyčius laiku."
        ),
        (
            "Tomato___Bacterial_spot",
            "Bakterinės dėmės plinta per vandenį, lietų ir tiesioginį kontaktą su kitais augalais ar įrankiais. "
            "Pažeistus lapus bei vaisius rekomenduojama pašalinti, o įrankius – dezinfekuoti prieš naudojimą. "
            "Venkite laistymo ant lapų ir naudokite vario pagrindu pagamintus preparatus kaip profilaktinę priemonę."
        ),
        (
            "Tomato___Spider_mites Two-spotted_spider_mite",
            "Duotaškiai voratinkliniai erkės gali sukelti stiprius lapų pažeidimus. "
            "Rekomenduojama purkšti augalus vandeniu, kad sumažintumėte erkių populiaciją, arba naudoti natūralius insekticidus, pavyzdžiui, neem aliejų. "
            "Taip pat būtina reguliariai apžiūrėti lapų apatinę pusę ir palaikyti pakankamą oro drėgmę aplink augalus."
        ),
        (
            "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
            "Šį virusą dažniausiai platina baltasparniai vabzdžiai. "
            "Pažeisti augalai turėtų būti pašalinti, o nuo baltasparnių rekomenduojama naudoti lipnias gaudykles ar biologines kontrolės priemones. "
            "Siekiant apsaugoti sveikus augalus, būtina reguliariai tikrinti augalus ir vengti jų tankaus susodinimo."
        )
    ]

    for klase, tekstas in patarimai:
        sesija.add(PatarimasPagalKlase(klase=klase, patarimas=tekstas))
    sesija.commit()


# --------------------------------------------------------------------------------------------------------------

class TestoRezultatas(Bazine_klase):
    __tablename__ = "testo_rezultatai"

    id = Column(Integer, primary_key=True)
    paveikslelis = Column(String)
    prognoze = Column(String)
    tikslumas = Column(String)
    modelis = Column(String)
    naudotojas = Column(String, default="anonimas")

def irasyti_testo_rezultata(paveikslelis, prognoze,tikslumas, modelis, naudotojas="anonimas"):

    _, _, sesija = sukurti_sesija()

    naujas_rezultatas = TestoRezultatas(paveikslelis=paveikslelis,prognoze=prognoze,tikslumas = tikslumas,
                                        modelis=modelis,naudotojas=naudotojas)

    sesija.add(naujas_rezultatas)
    sesija.commit()





# rysys_su_baze = create_engine('sqlite:///duomenu_baze/pomidoru_lapai.db')

# PomidoraiTrenyravimasHSV.__table__.drop(rysys_su_baze)
# PomidoraiValidacijaHSV.__table__.drop(rysys_su_baze)
# PomidoraiTestasHSV.__table__.drop(rysys_su_baze)
# print("Lentelė ištrinta.")



