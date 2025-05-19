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
    tikslumas = float(np.max(tikslumai))  # ne softmax, bet įvertinimas

    return klases[spejimas], tikslumas


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

    return render_template('pagrindinis.html', rezultatas=rezultatas, paveikslelis=paveikslelio_kelias)




if __name__ == '__main__':
    app.run(debug=True)