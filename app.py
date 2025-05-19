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
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
from prognozavimas_vartotojui import ( prognozuoti_su_cnn,prognozuoti_su_svc,prognozuoti_su_mobilenet,prognozuoti_su_cnn_hsv,prognozuoti_su_atsiustu_modeliu)

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

                klase, tikslumas = prognozuoti_su_atsiustu_modeliu(pilnas_kelias, klases_importuotas)
                rezultatas = f"Kito modelis: {klase} (tikslumas: {tikslumas*100:.2f}%)"

    return render_template('pagrindinis.html', rezultatas=rezultatas, paveikslelis=paveikslelio_kelias)




if __name__ == '__main__':
    app.run(debug=True)