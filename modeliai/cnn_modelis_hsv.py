import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import load_img, img_to_array, to_categorical
from duomenu_apdorojimas.db_ir_irasymas import sukurti_sesija
from duomenu_apdorojimas.paveiksleliu_nuskaitymas import issitraukti_paveikslelius, uzkoduoti_klases_lable

rysys_su_baze, Session, sesija = sukurti_sesija()

train_df = pd.read_sql_table('Pomidoru_lapai_trenyravimo_hsv', con=rysys_su_baze)
val_df = pd.read_sql_table('Pomidoru_lapai_validacijos_hsv', con=rysys_su_baze)
test_df = pd.read_sql_table('Pomidoru_lapai_testo_hsv', con=rysys_su_baze)

x_train, y_train = issitraukti_paveikslelius(train_df, dydis=(128, 128))
x_val, y_val = issitraukti_paveikslelius(val_df, dydis=(128, 128))
x_test, y_test = issitraukti_paveikslelius(test_df, dydis=(128, 128))


y_train, y_val, y_test = uzkoduoti_klases_lable(y_train, y_val, y_test)
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
        layers.Conv2D(64, (3, 3), activation='relu', input_shape=ivesties_forma),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.4),

        layers.Conv2D(32, (3, 3), activation='relu'),
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
sustabdymas = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

history = modelis.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=40, callbacks=[sustabdymas])

nuostolis, tikslumas = modelis.evaluate(x_test, y_test, verbose=1)
print(f"Testo nuostolis: {nuostolis:.4f}")
print(f"Testo tikslumas: {tikslumas:.4f}")

modelis.save("issaugoti_modeliai/hsv_cnn_modelis.h5")