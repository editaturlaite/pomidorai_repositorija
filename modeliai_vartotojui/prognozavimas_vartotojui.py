import numpy as np
import cv2
import joblib
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from skimage.color import rgb2gray
from skimage.feature import hog
from scipy.special import softmax


def prognozuoti_su_cnn(nuotraukos_kelias, klases, dydis=(128, 128)):
    try:
        modelis = load_model("modeliai_vartotojui/issaugoti_modeliai/paprastas_cnn_962.h5")

        atidarytas_paveikslelis = load_img(nuotraukos_kelias, target_size=dydis)
        paveikslelis_array = img_to_array(atidarytas_paveikslelis)
        paveikslelis_array = np.expand_dims(paveikslelis_array, axis=0) #pridedamas bach dydis 1 (128.128.3)(1.128.128.3)

        prognozes_klasems = modelis.predict(paveikslelis_array)
        klase = np.argmax(prognozes_klasems)
        tikslumas = float(np.max(prognozes_klasems))

        return klases[klase], tikslumas
    
    except Exception as klaida:
        raise RuntimeError(f"CNN modelio klaida")

def prognozuoti_su_svc(nuotraukos_kelias, klases, dydis=(128, 128)):
    try:
        modelis = joblib.load("modeliai_vartotojui/issaugoti_modeliai/svc_modelis_rbf.pkl")

        atidarytas_paveikslelis = cv2.imread(nuotraukos_kelias)

        paveikslelis_i_rgb = cv2.cvtColor(atidarytas_paveikslelis, cv2.COLOR_BGR2RGB)

        sumazintas_paveikslelis = cv2.resize(paveikslelis_i_rgb, dydis)

        pilkas_paveikslelis = rgb2gray(sumazintas_paveikslelis / 255.0)

        pozymiai = hog(
            pilkas_paveikslelis,
            pixels_per_cell=(16, 16),
            cells_per_block=(3, 3),
            orientations=9,
            feature_vector=True).reshape(1, -1)

        spejimas = modelis.predict(pozymiai)[0]
        tikslumai = modelis.decision_function(pozymiai)
        procentai = softmax(tikslumai)[0]  # paverčiam į tikimybes
        tikslumas = float(np.max(procentai))

        return klases[spejimas], tikslumas
   
    except Exception as klaida:
        raise RuntimeError(f"SVC modelio klaida")


def prognozuoti_su_mobilenet(nuotraukos_kelias, klases, dydis=(224, 224)):
    try:
        modelis = load_model("modeliai_vartotojui/issaugoti_modeliai/mobilenet_modelis.h5") 

        atidarytas_paveikslelis = load_img(nuotraukos_kelias, target_size=dydis)
        paveikslelis_array = img_to_array(atidarytas_paveikslelis) # masyvas (224, 224, 3)
        paveikslelis_array = np.expand_dims(paveikslelis_array, axis=0) #pridedamas bach dydis 1 (128.128.3)(1.128.128.3)

        prognozes_klasems = modelis.predict(paveikslelis_array)
        klase = np.argmax(prognozes_klasems)
        tikslumas = float(np.max(prognozes_klasems))

        return klases[klase], tikslumas
    
    except Exception as klaida:
        raise RuntimeError(f"MobileNet modelio klaida")

def prognozuoti_su_cnn_hsv(nuotraukos_kelias, klases, dydis=(128, 128)):
    try:
        modelis = load_model("modeliai_vartotojui/issaugoti_modeliai/cnn_hsv_modelis.h5")

        atidarytas_paveikslelis = cv2.imread(nuotraukos_kelias)
        paveikslelis_rgb = cv2.cvtColor(atidarytas_paveikslelis, cv2.COLOR_BGR2RGB)
        sumazintas_paveikslelis = cv2.resize(paveikslelis_rgb, dydis)

        paveikslelis_array = np.expand_dims(sumazintas_paveikslelis, axis=0)

        prognozes_klasems = modelis.predict(paveikslelis_array)
        klase = np.argmax(prognozes_klasems)
        tikslumas = float(np.max(prognozes_klasems))

        return klases[klase], tikslumas
    
    except Exception as klaida:
        raise RuntimeError(f"CNN HSV modelio klaida")


def prognozuoti_su_atsiustu_modeliu(nuotraukos_kelias, klases, dydis=(256, 256)):
    try:
        modelis = load_model("modeliai_vartotojui/issaugoti_modeliai/kagle_modelis.h5")

        atidarytas_paveikslelis = load_img(nuotraukos_kelias, target_size=dydis)
        paveikslelis_array = img_to_array(atidarytas_paveikslelis)
        paveikslelis_array = np.expand_dims(paveikslelis_array, axis=0)
        paveikslelis_array = paveikslelis_array / 255.0  

        prognozes_klasems = modelis.predict(paveikslelis_array)
        klase = np.argmax(prognozes_klasems)
        tikslumas = float(np.max(prognozes_klasems))

        return klases[klase], tikslumas
    
    except Exception as klaida:
        raise RuntimeError(f"Kaggle modelio klaida")