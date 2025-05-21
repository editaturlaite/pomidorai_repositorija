import os
import cv2
from PIL import Image
import numpy as np



# def konvertuoti_i_hsv(pav_failo_kelias):
#     paveikslelis = cv2.imread(pav_failo_kelias)
#     paveikslelis = cv2.cvtColor(paveikslelis, cv2.COLOR_BGR2RGB)
#     hsv_paveikslelis = cv2.cvtColor(paveikslelis, cv2.COLOR_RGB2HSV)
#     return hsv_paveikslelis

# def issaugoti_hsv_paveiksleli(hsv_masyvas, issaugojimo_kelias):
#     rgb_masyvas = cv2.cvtColor(hsv_masyvas, cv2.COLOR_HSV2RGB)
#     paveikslelis = Image.fromarray(rgb_masyvas)
#     paveikslelis.save(issaugojimo_kelias)

# def konvertuoti_viska_i_hsv(pradinis_kelias, issaugojimo_kelias):
#     for aplanko_kelias in ["trenyravimas", "validacija", "testas"]:
#         pilno_aplanko_kelias = os.path.join(pradinis_kelias, aplanko_kelias)
#         naujo_aplanko_kelias = os.path.join(issaugojimo_kelias, aplanko_kelias)

#         for klases_kelias in os.listdir(pilno_aplanko_kelias):
#             pradzios_klases_aplanko_kelias= os.path.join(pilno_aplanko_kelias, klases_kelias)
#             naujos_klases_aplanko_kelias = os.path.join(naujo_aplanko_kelias, klases_kelias)
#             os.makedirs(naujos_klases_aplanko_kelias, exist_ok=True)

#             for failo_pavadinimo_kelias in os.listdir(pradzios_klases_aplanko_kelias):
#                 if failo_pavadinimo_kelias.lower().endswith(('.jpg', '.png', '.jpeg')):
#                     pilnas_failo_kelias = os.path.join(pradzios_klases_aplanko_kelias, failo_pavadinimo_kelias)
#                     hsv_paveikslelis = konvertuoti_i_hsv(pilnas_failo_kelias)
#                     pilnas_kelias_issaugojimui = os.path.join(naujos_klases_aplanko_kelias, failo_pavadinimo_kelias)
#                     issaugoti_hsv_paveiksleli(hsv_paveikslelis, pilnas_kelias_issaugojimui)

# ----------------------------------------------------------------------------------------------------------------------

def konvertuoti_i_hsv(pav_failo_kelias):
    paveikslelis = cv2.imread(pav_failo_kelias)
    paveikslelis = cv2.cvtColor(paveikslelis, cv2.COLOR_BGR2RGB)
    hsv_paveikslelis = cv2.cvtColor(paveikslelis, cv2.COLOR_RGB2HSV)
    return hsv_paveikslelis


def issaugoti_hsv_numpy(hsv_masyvas, issaugojimo_kelias): #taisyklinai
    np.save(issaugojimo_kelias, hsv_masyvas)



def konvertuoti_viska_i_hsv_taisyklingai(pradinis_kelias, issaugojimo_kelias):
    for aplanko_kelias in ["trenyravimas", "validacija", "testas"]:
        pilno_aplanko_kelias = os.path.join(pradinis_kelias, aplanko_kelias)
        naujo_aplanko_kelias = os.path.join(issaugojimo_kelias, aplanko_kelias)

        for klases_kelias in os.listdir(pilno_aplanko_kelias):
            pradzios_klases_aplanko_kelias= os.path.join(pilno_aplanko_kelias, klases_kelias)
            naujos_klases_aplanko_kelias = os.path.join(naujo_aplanko_kelias, klases_kelias)
            os.makedirs(naujos_klases_aplanko_kelias, exist_ok=True)

            for failo_pavadinimo_kelias in os.listdir(pradzios_klases_aplanko_kelias):
                if failo_pavadinimo_kelias.lower().endswith(('.jpg', '.png', '.jpeg')):
                    pilnas_failo_kelias = os.path.join(pradzios_klases_aplanko_kelias, failo_pavadinimo_kelias)
                    hsv_paveikslelis = konvertuoti_i_hsv(pilnas_failo_kelias)
                    failo_kelias = os.path.join(naujos_klases_aplanko_kelias, failo_pavadinimo_kelias.split('.')[0])
                    issaugoti_hsv_numpy(hsv_paveikslelis, failo_kelias)