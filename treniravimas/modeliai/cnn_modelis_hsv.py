import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.utils import  to_categorical
from duomenu_apdorojimas.paruosti_duomenys_hsv import x_train, y_train, x_val, y_val, x_test, y_test
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay


y_train = to_categorical(y_train)
y_val = to_categorical(y_val)
y_test = to_categorical(y_test)


x_train = x_train.astype("float32") / 255.0
x_val = x_val.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0


klasiu_skaicius = y_train.shape[1]
ivesties_forma = (128, 128, 3)
SEED = 42


def sukurti_cnn_hsv(ivesties_forma, klasiu_skaicius, learning_rate=0.0001):
    modelis = keras.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=ivesties_forma),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        # layers.Dropout(0.4),

        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.4),

        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.4),
        layers.Dense(klasiu_skaicius, activation='softmax')])

    optimizieris = keras.optimizers.Adam(learning_rate=learning_rate)
    modelis.compile(optimizer=optimizieris, loss='categorical_crossentropy', metrics=['accuracy'])

    return modelis

modelis = sukurti_cnn_hsv(ivesties_forma, klasiu_skaicius)
sustabdymas = EarlyStopping(monitor='val_loss', patience=8, restore_best_weights=True)

history = modelis.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=50, callbacks=[sustabdymas])

nuostolis, tikslumas = modelis.evaluate(x_test, y_test, verbose=1)
print(f"Testo nuostolis: {nuostolis:.4f}")
print(f"Testo tikslumas: {tikslumas:.4f}")


y_tikros = np.argmax(y_test, axis=1)
y_prognozes = np.argmax(modelis.predict(x_test), axis=1)

matrica = confusion_matrix(y_tikros, y_prognozes)
disp = ConfusionMatrixDisplay(confusion_matrix=matrica)
disp.plot(xticks_rotation=45, cmap="Blues")
plt.title("HSV CNN Matrica")
plt.tight_layout()
plt.show()

print(classification_report(y_tikros, y_prognozes))

modelis.save("modeliai_vartotojui/issaugoti_modeliai/hsv_cnn_modelis_taisyklingai.h5")