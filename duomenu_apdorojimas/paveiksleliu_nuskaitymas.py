from tensorflow.keras.utils import load_img, img_to_array,to_categorical 
from sklearn.preprocessing import LabelEncoder
import numpy as np


def issitraukti_paveikslelius(df, dydis=(128, 128)):
    paveiksleliai = []
    klasifikacijos = []

    for indeksas, eilute in df.iterrows():
        paveikslelis = load_img(eilute['kelias'], target_size=dydis)
        paveikslelis_array = img_to_array(paveikslelis)
        paveiksleliai.append(paveikslelis_array)
        klasifikacijos.append(eilute['klases_pavadinimas'])

    return np.array(paveiksleliai), np.array(klasifikacijos)

def uzkoduoti_klases_lable(y_train, y_val, y_test):
    
    enkoderis = LabelEncoder()
    y_train_skaiciais = enkoderis.fit_transform(y_train)
    y_val_skaiciais = enkoderis.transform(y_val)
    y_test_skaiciais = enkoderis.transform(y_test)

    return y_train_skaiciais, y_val_skaiciais, y_test_skaiciais

def uzkoduoti_klases_lable_onehot(y_train, y_val, y_test):

    enkoderis = LabelEncoder()
    y_train_skaiciais = enkoderis.fit_transform(y_train)
    y_val_skaiciais = enkoderis.transform(y_val)
    y_test_skaiciais = enkoderis.transform(y_test)
    y_train_kategorijos = to_categorical(y_train_skaiciais)
    y_val_kategorijos = to_categorical(y_val_skaiciais)
    y_test_kategorijos = to_categorical(y_test_skaiciais)

    return y_train_kategorijos, y_val_kategorijos, y_test_kategorijos