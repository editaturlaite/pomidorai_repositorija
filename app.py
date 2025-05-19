from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import joblib
from skimage.color import rgb2gray
from skimage.feature import hog
import cv2
from scipy.special import softmax


def prognozuoti_su_cnn(nuotraukos_kelias, klases, dydis=(128, 128)):
    modelis = load_model("issaugoti_modeliai/paprastas_cnn_962.h5")

    atidarytas_paveikslelis = load_img(nuotraukos_kelias, target_size=dydis)
    paveikslelis_array = img_to_array(atidarytas_paveikslelis)
    paveikslelis_array = np.expand_dims(paveikslelis_array, axis=0) #pridedamas bach dydis 1 (128.128.3)(1.128.128.3)

    prognozes = modelis.predict(paveikslelis_array)
    klase = np.argmax(prognozes)
    tikslumas = float(np.max(prognozes))

    return klases[klase], tikslumas

def prognozuoti_su_svc(nuotraukos_kelias, klases, dydis=(128, 128)):
    # Įkeliame modelį
    modelis = joblib.load("issaugoti_modeliai/svc_modelis_rbf.pkl")

    # Apdorojam paveikslėlį
    img_bgr = cv2.imread(nuotraukos_kelias)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(img_rgb, dydis)

    img_gray = rgb2gray(img_resized / 255.0)

    pozymiai = hog(
        img_gray,
        pixels_per_cell=(16, 16),
        cells_per_block=(3, 3),
        orientations=9,
        feature_vector=True
    ).reshape(1, -1)

    spejimas = modelis.predict(pozymiai)[0]
    tikslumai = modelis.decision_function(pozymiai)
    procentai = softmax(tikslumai)[0]  # paverčiam į tikimybes
    tikslumas = float(np.max(procentai))

    return klases[spejimas], tikslumas

def prognozuoti_su_mobilenet(nuotraukos_kelias, klases, dydis=(224, 224)):
    modelis = load_model("issaugoti_modeliai/mobilenet_modelis.h5") 

    img = load_img(nuotraukos_kelias, target_size=dydis)
    paveikslelis_array = img_to_array(img)
    paveikslelis_array = np.expand_dims(paveikslelis_array, axis=0)

    prognozes = modelis.predict(paveikslelis_array)
    klase = np.argmax(prognozes)
    tikslumas = float(np.max(prognozes))

    return klases[klase], tikslumas

def prognozuoti_su_cnn_hsv(nuotraukos_kelias, klases, dydis=(128, 128)):

    modelis = load_model("issaugoti_modeliai/cnn_hsv_modelis.h5")

    img_bgr = cv2.imread(nuotraukos_kelias)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)
    img_resized = cv2.resize(img_hsv, dydis)

    img_array = np.expand_dims(img_resized, axis=0)

    prognozes = modelis.predict(img_array)
    klase = np.argmax(prognozes)
    tikslumas = float(np.max(prognozes))

    return klases[klase], tikslumas

def prognozuoti_su_importuotu_modeliu(nuotraukos_kelias, klases, dydis=(256, 256)):
    from tensorflow.keras.models import load_model
    from tensorflow.keras.preprocessing.image import load_img, img_to_array
    import numpy as np

    modelis = load_model("issaugoti_modeliai/importuotas_modelis.h5")

    img = load_img(nuotraukos_kelias, target_size=dydis)
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # normalizavimas, jei modelyje nėra Rescaling sluoksnio

    prognozes = modelis.predict(img_array)
    klase = np.argmax(prognozes)
    tikslumas = float(np.max(prognozes))

    return klases[klase], tikslumas


app = Flask(__name__)

# Nustatome aplanką įkeliamiems failams
UPLOAD_FOLDER = 'static/ikelti_paveiksleliai'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():

    rezultatas = None
    paveikslelio_kelias = None

    klases = [
        'Tomato___Bacterial_spot',
        'Tomato___Late_blight',
        'Tomato___Septoria_leaf_spot',
        'Tomato___Spider_mites Two-spotted_spider_mite',
        'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
        'Tomato___healthy']

    if request.method == 'POST':

        pasirinktas_modelis = request.form['modelis']
        failas = request.files['nuotrauka']

        if failas:
            failo_vardas = secure_filename(failas.filename)
            pilnas_kelias = os.path.join(app.config['UPLOAD_FOLDER'], failo_vardas)
            failas.save(pilnas_kelias)
            paveikslelio_kelias = pilnas_kelias 

            if pasirinktas_modelis == 'cnn':

                klase, tikslumas = prognozuoti_su_cnn(pilnas_kelias, klases)

                rezultatas = f"CNN modelis: {klase} (tikslumas: {tikslumas*100:.2f}%)"

            elif pasirinktas_modelis == 'svc':

                klase, tikslumas = prognozuoti_su_svc(pilnas_kelias, klases)

                rezultatas = f"SVC modelis: {klase} (modelio įsitikinimas: {tikslumas:.2f})"

            elif pasirinktas_modelis == 'mobilenet':

                klase, tikslumas = prognozuoti_su_mobilenet(pilnas_kelias, klases)

                rezultatas = f"MobileNet modelis: {klase} (tikslumas: {tikslumas*100:.2f}%)"

            elif pasirinktas_modelis == 'cnn_hsv':

                klase, tikslumas = prognozuoti_su_cnn_hsv(pilnas_kelias, klases)

                rezultatas = f"CNN HSV modelis: {klase} (tikslumas: {tikslumas*100:.2f}%)"

            elif pasirinktas_modelis == 'parsiustas':

                klases_importuotas = [
                    'Tomato___Bacterial_spot',
                    'Tomato___Early_blight',
                    'Tomato___Late_blight',
                    'Tomato___Leaf_Mold',
                    'Tomato___Septoria_leaf_spot',
                    'Tomato___Spider_mites Two-spotted_spider_mite',
                    'Tomato___Target_Spot',
                    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
                    'Tomato___Tomato_mosaic_virus',
                    'Tomato___healthy']

                klase, tikslumas = prognozuoti_su_importuotu_modeliu(pilnas_kelias, klases_importuotas)
                rezultatas = f"Kito modelis: {klase} (tikslumas: {tikslumas*100:.2f}%)"

    return render_template('pagrindinis.html', rezultatas=rezultatas, paveikslelis=paveikslelio_kelias)




if __name__ == '__main__':
    app.run(debug=True)