from modeliai.paprastas_cnn import sukurti_paprasta_cnn
from tensorflow.keras.callbacks import EarlyStopping
from duomenu_apdorojimas.paruosti_duomenys import (x_train, y_train, x_val, y_val, x_test, y_test)
from duomenu_apdorojimas.paveiksleliu_nuskaitymas import uzkoduoti_klases_lable_onehot
from modeliai.svc_modelis import uzkrauti_svc_modeli
from sklearn.metrics import classification_report, accuracy_score

# ---------------------------------------------------------------------------------------------------------------------
# SVC modelis

modelis = uzkrauti_svc_modeli()
y_spejimai = modelis.predict(x_test)

print("Tikslumas:", accuracy_score(y_test, y_spejimai))

print(classification_report(y_test, y_spejimai))


# ---------------------------------------------------------------------------------------------------------------
# Paprastas CNN

# from tensorflow.keras.models import load_model
# modelis = load_model("modeliai/cnn_modelis.h5")

# ---------------------------------------------------------------------------------------