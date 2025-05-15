from tensorflow.keras.utils import load_img, img_to_array
from sklearn.preprocessing import LabelEncoder
import numpy as np

def issitraukti_paveikslelius(df, dydis=(224, 224)):
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