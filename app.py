from flask import Flask, render_template, request,redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from modeliai_vartotojui.prognozavimas_vartotojui import ( prognozuoti_su_cnn,prognozuoti_su_svc,prognozuoti_su_mobilenet,prognozuoti_su_cnn_hsv,prognozuoti_su_atsiustu_modeliu)
from duomenu_apdorojimas.db_ir_irasymas import sukurti_sesija, irasyti_ikelta_paveiksleli
from duomenu_apdorojimas.db_ir_irasymas import IkeltaPaveikslelis
from sqlalchemy import create_engine
from duomenu_apdorojimas.db_ir_irasymas import Bazine_klase, sukurti_sesija, sukurti_patarimus,irasyti_testo_rezultata
from duomenu_apdorojimas.db_ir_irasymas import PatarimasPagalKlase,TestoRezultatas


app = Flask(__name__)
app.secret_key = 'saugos_raktas'  # būtina flash žinutėms


# # a[lankas] įkeliamiems failams
VARTOTOJU_PAVEIKSLELIAI = 'static/ikelti_paveiksleliai'
os.makedirs(VARTOTOJU_PAVEIKSLELIAI, exist_ok=True)
app.config['UPLOAD_FOLDER'] = VARTOTOJU_PAVEIKSLELIAI

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
            try:
                failo_vardas = secure_filename(failas.filename)
                pilnas_kelias = os.path.join(app.config['UPLOAD_FOLDER'], failo_vardas)
                failas.save(pilnas_kelias)
                paveikslelio_kelias = pilnas_kelias 

                _, _, sesija = sukurti_sesija()
                irasyti_ikelta_paveiksleli(sesija, pilnas_kelias)

                paskutinis_ikeltas = sesija.query(IkeltaPaveikslelis).order_by(IkeltaPaveikslelis.id.desc()).first()
                paveikslelio_kelias = paskutinis_ikeltas.kelias

                if pasirinktas_modelis == 'cnn':

                    klase, tikslumas = prognozuoti_su_cnn(pilnas_kelias, klases)

                    irasyti_testo_rezultata(paveikslelis=paveikslelio_kelias,prognoze=klase,tikslumas=tikslumas,modelis="cnn")

                    try:
                        patarimo_tekstas = sesija.query(PatarimasPagalKlase).filter_by(klase=klase).first().patarimas
                    except:
                        patarimo_tekstas = "Profilaktinės rekomendacijos šiai klasei nėra"

                    rezultatas = (f"CNN modelis: {klase} (tikslumas/pasitikėjimas šiam spėjimui: {tikslumas*100:.2f}%) <br><br>"
                    f"Profilaktinė rekomendacija: <br><br>{patarimo_tekstas}")


                elif pasirinktas_modelis == 'svc':

                    klase, tikslumas = prognozuoti_su_svc(pilnas_kelias, klases)

                    irasyti_testo_rezultata(paveikslelis=paveikslelio_kelias,prognoze=klase,tikslumas=tikslumas,modelis="svc")

                    try:
                        patarimo_tekstas = sesija.query(PatarimasPagalKlase).filter_by(klase=klase).first().patarimas
                    except:
                        patarimo_tekstas = "Profilaktinės rekomendacijos šiai klasei nėra"

                    rezultatas = (f"SVC modelis: {klase} (modelio įsitikinimas šiam spėjimui: {tikslumas:.2f}) <br><br>"
                    f"Profilaktinė rekomendacija: <br><br>{patarimo_tekstas}")

                elif pasirinktas_modelis == 'mobilenet':

                    klase, tikslumas = prognozuoti_su_mobilenet(pilnas_kelias, klases)
                    irasyti_testo_rezultata(paveikslelis=paveikslelio_kelias,prognoze=klase,tikslumas=tikslumas,modelis="mobilenet")

                    try:
                        patarimo_tekstas = sesija.query(PatarimasPagalKlase).filter_by(klase=klase).first().patarimas
                    except:
                        patarimo_tekstas = "Profilaktinės rekomendacijos šiai klasei nėra"

                    rezultatas = (f"MobileNet modelis: {klase} (tikslumas/pasitikėjimas šiam spėjimui: {tikslumas*100:.2f}%)<br><br>"
                    f"Profilaktinė rekomendacija: <br><br>{patarimo_tekstas}")

                elif pasirinktas_modelis == 'cnn_hsv':

                    klase, tikslumas = prognozuoti_su_cnn_hsv(pilnas_kelias, klases)

                    irasyti_testo_rezultata(paveikslelis=paveikslelio_kelias,prognoze=klase,tikslumas=tikslumas,modelis="cnn_hsv")

                    try:
                        patarimo_tekstas = sesija.query(PatarimasPagalKlase).filter_by(klase=klase).first().patarimas
                    except:
                        patarimo_tekstas = "Profilaktinės rekomendacijos šiai klasei nėra"

                    rezultatas = (f"CNN HSV modelis: {klase} (tikslumas/pasitikėjimas šiam spėjimui: {tikslumas*100:.2f}%)<br><br>"
                    f"Profilaktinė rekomendacija: <br><br>{patarimo_tekstas}")

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

                    irasyti_testo_rezultata(paveikslelis=paveikslelio_kelias,prognoze=klase,tikslumas=tikslumas,modelis="Kaggle")

                    try:
                        patarimo_tekstas = sesija.query(PatarimasPagalKlase).filter_by(klase=klase).first().patarimas
                    except:
                        patarimo_tekstas = "Profilaktinės rekomendacijos šiai klasei nėra"

                    rezultatas = (f"Kaggle modelis: {klase} (tikslumas/pasitikėjimas šiam spėjimui: {tikslumas*100:.2f}%)<br><br>"
                    f"Profilaktinė rekomendacija: <br><br>{patarimo_tekstas}")

            except RuntimeError as klaida:
                rezultatas = klaida
            except Exception:
                rezultatas = "Klaida apdorojant failą"

    return render_template('pagrindinis.html', rezultatas=rezultatas, paveikslelis=paveikslelio_kelias)

@app.route('/ikelti_mokymui', methods=['GET', 'POST'])
def ikelti_mokymui():
    if request.method == 'POST':
        try:
            klase = request.form['klase']
            failas = request.files['nuotrauka']

            paveikslelio_pavadinimas = secure_filename(failas.filename)
            klase_aplankas = os.path.join('static', 'ikelta_mokymui', klase)
            os.makedirs(klase_aplankas, exist_ok=True)
            paveikslelio_kelias = os.path.join(klase_aplankas, paveikslelio_pavadinimas)
            failas.save(paveikslelio_kelias)

            flash(f" Nuotrauka įkelta į klasę: {klase}", "success")
            return redirect(url_for('ikelti_mokymui'))
        
        except Exception as klaida:
            flash("Klaida įkeliant failą", "error")
            return redirect(url_for('ikelti_mokymui'))

    return render_template('ikelti_mokymui.html')


if __name__ == '__main__':

    # engine = create_engine('sqlite:///duomenu_baze/pomidoru_lapai.db')
    # Bazine_klase.metadata.create_all(engine)

    # _, _, sesija = sukurti_sesija()
    # sukurti_patarimus(sesija)

    app.run(debug=True)
