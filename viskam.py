
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pandas as pd
import numpy as np
from tensorflow.keras.utils import load_img, img_to_array
from sklearn.preprocessing import LabelEncoder
from sqlalchemy import create_engine


train_kelias = r"C:\Users\Vartotojas\Desktop\POMIDORAI\pomidoru_duomenys\trenyravimas"
val_kelias = r"C:\Users\Vartotojas\Desktop\POMIDORAI\pomidoru_duomenys\validacija"
test_kelias = r"C:\Users\Vartotojas\Desktop\POMIDORAI\pomidoru_duomenys\testas"

train_df = tf.keras.utils.image_dataset_from_directory(train_kelias,image_size=(224, 224),batch_size=32)

val_df = tf.keras.utils.image_dataset_from_directory(val_kelias,image_size=(224, 224),batch_size=32)

test_df = tf.keras.utils.image_dataset_from_directory(test_kelias,image_size=(224, 224),batch_size=32)

# ---------------------------------------------------------

from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from sqlalchemy.orm import declarative_base

Bazine_klase = declarative_base()
rysys_su_baze = create_engine('sqlite:///pomidoru_lapai.db')

Session = sessionmaker(bind=rysys_su_baze)
sesija = Session()

# class PomidoraiTrenyravimas(Bazine_klase):

#     __tablename__ = 'Pomidoru_lapai_trenyravimo_duomenys'

#     id = Column(Integer,primary_key = True)
#     kelias = Column(String, unique=True, nullable=False)  
#     klases_pavadinimas = Column(String, nullable=False)


# def irasyti_trenyravimo_paveikslelius(sesija, trenyravimo_kelias):

#     for klases_pavadinimas in os.listdir(trenyravimo_kelias):
#         klases_kelias = os.path.join(trenyravimo_kelias,klases_pavadinimas)

#         if os.path.isdir(klases_kelias):
#             for paveikslelio_pavadinimas in os.listdir(klases_kelias):
#                 paveikslelio_kelias = os.path.join(klases_kelias,paveikslelio_pavadinimas)

#                 egzistuoja = sesija.query(PomidoraiTrenyravimas).filter_by(kelias=paveikslelio_kelias).first()

#                 if not egzistuoja:

#                     naujas_irasas = PomidoraiTrenyravimas(kelias = paveikslelio_kelias, klases_pavadinimas = klases_pavadinimas)

#                     sesija.add(naujas_irasas)

#     sesija.commit()

#     print("Irasyti trenyravimo paveiksleiai")

# # --------------------------------------------------------------------------------------------------------------------------


# class PomidoraiValidacija(Bazine_klase):

#     __tablename__ = 'Pomidoru_lapai_validacijos_duomenys'

#     id = Column(Integer,primary_key = True)
#     kelias = Column(String, unique=True, nullable=False)  
#     klases_pavadinimas = Column(String, nullable=False)

# def irasyti_validacijos_paveikslelius(sesija, validacijos_kelias):

#     for klases_pavadinimas in os.listdir(validacijos_kelias):
#         klases_kelias = os.path.join(validacijos_kelias,klases_pavadinimas)

#         if os.path.isdir(klases_kelias):
#             for paveikslelio_pavadinimas in os.listdir(klases_kelias):
#                 paveikslelio_kelias = os.path.join(klases_kelias,paveikslelio_pavadinimas)

#                 egzistuoja = sesija.query(PomidoraiValidacija).filter_by(kelias=paveikslelio_kelias).first()

#                 if not egzistuoja:

#                     naujas_irasas = PomidoraiValidacija(kelias = paveikslelio_kelias, klases_pavadinimas = klases_pavadinimas)

#                     sesija.add(naujas_irasas)

#     sesija.commit()

#     print("Irasyti validacijos paveiksleiai")

# # -------------------------------------------------------------------------------------------------------------

# class PomidoraiTestas(Bazine_klase):

#     __tablename__ = 'Pomidoru_lapai_testo_duomenys'

#     id = Column(Integer,primary_key = True)
#     kelias = Column(String, unique=True, nullable=False)  
#     klases_pavadinimas = Column(String, nullable=False)

# def irasyti_testo_paveikslelius(sesija, testo_kelias):

#     for klases_pavadinimas in os.listdir(test_kelias):
#         klases_kelias = os.path.join(test_kelias,klases_pavadinimas)

#         if os.path.isdir(klases_kelias):
#             for paveikslelio_pavadinimas in os.listdir(klases_kelias):
#                 paveikslelio_kelias = os.path.join(klases_kelias,paveikslelio_pavadinimas)

#                 egzistuoja = sesija.query(PomidoraiTestas).filter_by(kelias=paveikslelio_kelias).first()

#                 if not egzistuoja:

#                     naujas_irasas = PomidoraiTestas(kelias = paveikslelio_kelias, klases_pavadinimas = klases_pavadinimas)

#                     sesija.add(naujas_irasas)

#     sesija.commit()

#     print("Irasyti testo paveiksleiai")

# # ------------------------------------------------------------------------------------------
# Bazine_klase.metadata.create_all(rysys_su_baze)

# irasyti_trenyravimo_paveikslelius(sesija,train_kelias)
# irasyti_validacijos_paveikslelius(sesija,val_kelias)
# irasyti_testo_paveikslelius(sesija,test_kelias)

# ----------------------------------------------------------------------

train_df = pd.read_sql_table('Pomidoru_lapai_trenyravimo_duomenys', con=rysys_su_baze)

val_df = pd.read_sql_table('Pomidoru_lapai_validacijos_duomenys', con=rysys_su_baze)

test_df = pd.read_sql_table('Pomidoru_lapai_testo_duomenys', con=rysys_su_baze)


# print(train_df.head())
# print(val_df.head())
# print(test_df.head())

# ---------------------------------------------------------------------------------------------------

def issitraukti_paveikslelius(df, dydis=(224, 224)):
    paveiksleliai = []
    klasifikacijos = []

    for indeksas, eilute in df.iterrows():
        paveikslelis = load_img(eilute['kelias'], target_size=dydis)
        paveikslelis_array = img_to_array(paveikslelis)
        paveiksleliai.append(paveikslelis_array)
        klasifikacijos.append(eilute['klases_pavadinimas'])

    return np.array(paveiksleliai), np.array(klasifikacijos)

x_train, y_train = issitraukti_paveikslelius(train_df)
x_val, y_val = issitraukti_paveikslelius(val_df)
x_test, y_test = issitraukti_paveikslelius(test_df)



# ------------------------------------------------------------------------------------------------
# class_names = train_df.class_names
# print(class_names)

# for images, labels in train_df.take(1):
#     plt.figure(figsize=(10, 10))
#     for i in range(9):
#         ax = plt.subplot(3, 3, i + 1)
#         plt.imshow(images[i].numpy().astype("uint8"))
#         plt.title(class_names[labels[i]])
#         plt.axis("off")
#         # plt.show()

# ----------------------------------------------------------------

# print(train_df.class_names)


# class_names = train_df.class_names

# for images, labels in train_df.take(1):
#     plt.figure(figsize=(10, 10))
#     for i in range(9):
#         ax = plt.subplot(3, 3, i + 1)
#         plt.imshow(images[i].numpy().astype("uint8"))  # <-- jei vaizdas ryškus, gerai
#         plt.title(class_names[labels[i]])
#         plt.axis("off")
#     plt.tight_layout()
#     plt.show()

# print("Vieno paveikslėlio forma:", images[0].shape)



# ---------------------------------------------------------------------

# vietine duomenu augmentacija. vyksta realiu laiku visoms klasems. 

# duomenu_augmentacija = keras.Sequential([
#     layers.RandomFlip("horizontal"),
#     layers.RandomRotation(0.1),
#     layers.RandomZoom(0.1),
#     layers.RandomContrast(0.1),])

# augmentuota_train_df = train_df.map(lambda x, y: (duomenu_augmentacija(x, training = True),y),num_parallel_calls = tf.data.AUTOTUNE)

# -----------------------------------------------------------------------------

# fizine duomenu augmentacija

# import os
# from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img, save_img
# import numpy as np
# import random


# def sukurti_naujus_paveikslelius(duomenu_kelias, reikiamas_foto_kiekis):

#     failu_generavimas = ImageDataGenerator(
#         rotation_range=20,
#         width_shift_range=0.1,
#         height_shift_range=0.1,
#         zoom_range=0.1,
#         horizontal_flip=True,
#         fill_mode='nearest'
#     )

#     for klase in os.listdir(duomenu_kelias): #pereina per visas klases foldery
#         klases_kelias = os.path.join(duomenu_kelias, klase) #sujungia pagrindini kelia su konkrecia klase ir sukuria jos kelia 

#         try:
#             esami_failai = [f for f in os.listdir(klases_kelias) if f.endswith('.JPG')] # imamas kiekvienas failas f klases folderi ir jei atitinka idedamas i sarasa
#             kiek_truksta = reikiamas_foto_kiekis - len(esami_failai) #apskaiciuojam kiek truksta iki 2000

#             if kiek_truksta <= 0:
#                 print(f"{klase} turi pakankamai paveiksleliu")
#                 continue

#             sukurta = 0
#             while sukurta < kiek_truksta:
#                 originalus_paveikslelis = random.choice(esami_failai) #paimamas atsitiktinis originalus paveikslelis
#                 paveikslelis_kelias = os.path.join(klases_kelias, originalus_paveikslelis) #sujungia klases kelia su paveiksleliu ir sukuriamas paveikslelio kelias
#                 paveikslelis = load_img(paveikslelis_kelias) #uzkraunamas paveikslelis
#                 x = img_to_array(paveikslelis) #paveikslelis paverciamas i numeri np masyva
#                 x = np.expand_dims(x, axis=0) #pavercia i batch (224, 224, 3) prideda nr kiek paveiksleliu partijoje (1,224, 224, 3) nes imagegeneration veikia tik taip 

#                 for batch in failu_generavimas.flow(x, batch_size=1): #pradeda generuoti naujus paveikslelius is 1 paveikslelio
#                     failo_pavadinimas = f"aug_{sukurta}_{originalus_paveikslelis}"
#                     pilnas_kelias = os.path.join(klases_kelias, failo_pavadinimas) #sukuriamas kelias iki naujo sugeneruoto paveikslelio
#                     save_img(pilnas_kelias, batch[0]) #batch[0] vienas paveikslelis kaip masyvas
#                     sukurta += 1
#                     if sukurta >= kiek_truksta:
#                         break

#             print(f"Klasei {klase} sukurta {sukurta} nauju paveiksleliu")

#         except Exception as klaida:
#             print("Klaida generuojant paveikslelius")


# reikiamas_foto_kiekis = 2000

# duomenu_kelias = r"C:\Users\Vartotojas\Desktop\POMIDORAI\pomidoru_duomenys\trenyravimas"

# sukurti_naujus_paveikslelius(duomenu_kelias,reikiamas_foto_kiekis)

# ---------------------------------------------------------------------------


