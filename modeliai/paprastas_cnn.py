import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.utils import to_categorical
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
import matplotlib.pyplot as plt
from duomenu_apdorojimas.paruosti_duomenys import x_train, y_train, x_val, y_val, x_test, y_test
from duomenu_apdorojimas.paveiksleliu_nuskaitymas import uzkoduoti_klases_lable_onehot

def sukurti_paprasta_cnn(ivesties_forma, klasiu_skaicius, learning_rate=0.0001):
    modelis = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=ivesties_forma),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),

        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.4),
        layers.Dense(klasiu_skaicius, activation='softmax')])

    optimizeris = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    modelis.compile(optimizer=optimizeris, loss='categorical_crossentropy', metrics=['accuracy'])
    return modelis


y_train, y_val, y_test = uzkoduoti_klases_lable_onehot(y_train, y_val, y_test)


klasiu_skaicius = y_train.shape[1]
ivesties_forma = (128, 128, 3)


modelis = sukurti_paprasta_cnn(ivesties_forma, klasiu_skaicius)

sustabdymas = EarlyStopping(monitor='val_loss', patience=8, restore_best_weights=True)

history = modelis.fit(x_train, y_train, validation_data=(x_val, y_val),
                      epochs=40, batch_size=32, callbacks=[sustabdymas])


nuostolis, tikslumas = modelis.evaluate(x_test, y_test, verbose=1)
print(f"Testo nuostolis: {nuostolis:.4f}")
print(f"Testo tikslumas: {tikslumas:.4f}")


y_pradines = np.argmax(y_test, axis=1)
y_prognoze = np.argmax(modelis.predict(x_test), axis=1)

klasiu_pavadinimai = ['Bacterial_spot', 'Late_blight', 'Septoria_leaf_spot','Spider_mites', 'Tomato_Yellow_Leaf_Curl_Virus', 'healthy']


matrica = confusion_matrix(y_pradines, y_prognoze)
disp = ConfusionMatrixDisplay(confusion_matrix=matrica, display_labels=klasiu_pavadinimai)
disp.plot(xticks_rotation=40, cmap='Blues')
plt.title("Paprastas CNN Matrica")
plt.tight_layout()
plt.show()


print(classification_report(y_pradines, y_prognoze, target_names=klasiu_pavadinimai, digits=4))