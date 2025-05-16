import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib
from tensorflow.keras import layers, models
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.utils import to_categorical
from sklearn.svm import SVC
from sklearn.metrics import (accuracy_score,classification_report,confusion_matrix,ConfusionMatrixDisplay)
from duomenu_apdorojimas.db_ir_irasymas import sukurti_sesija
from duomenu_apdorojimas.paveiksleliu_nuskaitymas import (issitraukti_paveikslelius,uzkoduoti_klases_lable,uzkoduoti_klases_lable_onehot)
from duomenu_apdorojimas.paruosti_duomenys import (x_train, y_train,x_val, y_val,x_test, y_test)
from duomenu_apdorojimas.hog_pozymiai import istraukti_hog
from modeliai.paprastas_cnn import sukurti_paprasta_cnn
from modeliai.svc_modelis import uzkrauti_svc_modeli
from modeliai import cnn_modelis_hsv

# ---------------------------------------------------------------------------------------------------------------------
# paprastas CNN modelis

rysys_su_baze, _, sesija = sukurti_sesija()
test_df = pd.read_sql_table("Pomidoru_lapai_testo_duomenys", con=rysys_su_baze)

x_test, y_test = issitraukti_paveikslelius(test_df, dydis=(128, 128))
y_test = uzkoduoti_klases_lable_onehot(y_test, y_test, y_test)[0]

x_test = x_test.astype("float32") / 255.0


modelis = load_model("issaugoti_modeliai/paprastas_cnn_modelis.h5")


y_spejimai = modelis.predict(x_test)
y_spejamos_klases = np.argmax(y_spejimai, axis=1)
y_tikros_klases = np.argmax(y_test, axis=1)


print("Tikslumas:", accuracy_score(y_tikros_klases, y_spejamos_klases))

klasiu_pavadinimai = ['Bacterial_spot', 'Late_blight', 'Septoria_leaf_spot','Spider_mites', 'Tomato_Yellow_Leaf_Curl_Virus', 'healthy']

print(classification_report(y_tikros_klases, y_spejamos_klases, target_names=klasiu_pavadinimai, digits=4))


conf_matrix = confusion_matrix(y_tikros_klases, y_spejamos_klases)
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=klasiu_pavadinimai)
disp.plot(xticks_rotation=40, cmap='Blues')
plt.title("Paprastas CNN Matrica")
plt.tight_layout()
plt.show()


# ---------------------------------------------------------------------------------------------------------------
# SVC modelis

rysys_su_baze, _, sesija = sukurti_sesija()
test_df = pd.read_sql_table("Pomidoru_lapai_testo_hsv", con=rysys_su_baze)

x_test, y_test = issitraukti_paveikslelius(test_df, dydis=(128, 128))
y_test = uzkoduoti_klases_lable(y_test, y_test, y_test)[0]
x_test_hog = istraukti_hog(x_test)


modelis = joblib.load("issaugoti_modeliai/svc_modelis_linear.pkl")

y_spejimai = modelis.predict(x_test_hog)


print("Tikslumas:", accuracy_score(y_test, y_spejimai))
print(classification_report(y_test, y_spejimai))

conf_matrix = confusion_matrix(y_test, y_spejimai)
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix)
disp.plot(xticks_rotation=45)
plt.title("SVC Matrica")
plt.tight_layout()
plt.show()

# ---------------------------------------------------------------------------------------
# CNN su HVC

rysys_su_baze, _, sesija = sukurti_sesija()

test_df = pd.read_sql_table('Pomidoru_lapai_testo_hsv', con=rysys_su_baze)

x_test, y_test = issitraukti_paveikslelius(test_df, dydis=(128, 128))

y_test = uzkoduoti_klases_lable(y_test, y_test, y_test)[0]  # imame tik pirmą grąžintą (testo)

y_test = to_categorical(y_test)

x_test = x_test.astype("float32") / 255.0

modelis = load_model("issaugoti_modeliai/hsv_cnn_modelis.h5")


y_spejimai = modelis.predict(x_test)
y_spejamos_klases = np.argmax(y_spejimai, axis=1)
y_tikros_klases = np.argmax(y_test, axis=1)


print("Tikslumas:", accuracy_score(y_tikros_klases, y_spejamos_klases))
print(classification_report(y_tikros_klases, y_spejamos_klases))

conf_matrix = confusion_matrix(y_tikros_klases, y_spejamos_klases)
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix)
disp.plot(xticks_rotation=45)
plt.title("HSV CNN Matrica")
plt.tight_layout()
plt.show()
