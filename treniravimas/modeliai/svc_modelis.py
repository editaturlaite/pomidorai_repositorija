import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from duomenu_apdorojimas.hog_pozymiai import istraukti_hog
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from duomenu_apdorojimas.paruosti_duomenys import (x_train, y_train, x_val, y_val, x_test, y_test)
import matplotlib.pyplot as plt
import joblib

x_train_hog = istraukti_hog(x_train)
x_val_hog = istraukti_hog(x_val)
x_test_hog = istraukti_hog(x_test)

modelis = SVC(kernel='rbf')
modelis.fit(x_train_hog, y_train)

y_val_spejimai = modelis.predict(x_val_hog)
print("Tikslumas validacijos:", accuracy_score(y_val, y_val_spejimai))
print(classification_report(y_val, y_val_spejimai))

y_test_spejimai = modelis.predict(x_test_hog)
print("Tikslumas testo:", accuracy_score(y_test, y_test_spejimai))
print(classification_report(y_test, y_test_spejimai))


conf_matrix = confusion_matrix(y_test, y_test_spejimai)
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix)
disp.plot(xticks_rotation=45,cmap="Blues")
plt.title("SVC Matrica")
plt.tight_layout()
plt.show()


joblib.dump(modelis, r"C:\Users\Vartotojas\Desktop\POMIDORAI\pomidorai_repositorija\issaugoti_modeliai\svc_modelis_rbf.pkl")

# joblib.dump(modelis, "svc_modelis_linear.pkl") #colab