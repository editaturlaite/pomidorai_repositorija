import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.utils import class_weight
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

paveikslelio_dydis = (224, 224)
batch_size = 32
SEED = 42

train_ds = tf.keras.utils.image_dataset_from_directory(
    r"C:\Users\Vartotojas\Desktop\POMIDORAI\pomidoru_duomenys\trenyravimas",
    image_size=paveikslelio_dydis,
    batch_size=batch_size,
    label_mode="int",
    shuffle=True,
    seed=SEED)

val_ds = tf.keras.utils.image_dataset_from_directory(
    r"C:\Users\Vartotojas\Desktop\POMIDORAI\pomidoru_duomenys\validacija",
    image_size=paveikslelio_dydis,
    batch_size=batch_size,
    label_mode="int",
    shuffle=False,
    seed=SEED)

test_ds = tf.keras.utils.image_dataset_from_directory(
    r"C:\Users\Vartotojas\Desktop\POMIDORAI\pomidoru_duomenys\testas",
    image_size=paveikslelio_dydis,
    batch_size=batch_size,
    label_mode="int",
    shuffle=False,
    seed=SEED)


ivesties_forma = (224, 224, 3)
klasiu_skaicius = len(train_ds.class_names)

mobilenet_pagrindas = MobileNetV2(
    input_shape=ivesties_forma,
    include_top=False,
    weights='imagenet')

mobilenet_pagrindas.trainable = False

modelis = models.Sequential([
    layers.Rescaling(1./255, input_shape=ivesties_forma),
    mobilenet_pagrindas,
    layers.GlobalAveragePooling2D(),
    layers.Dense(180, activation='relu'),
    layers.BatchNormalization(),
    layers.Dropout(0.4),
    layers.Dense(100, activation='relu'),
    layers.Dropout(0.4),
    layers.Dense(klasiu_skaicius, activation='softmax')])

modelis.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.00008),loss='sparse_categorical_crossentropy',metrics=['accuracy'])


klasiu_svoriai = {0: 1.0,1: 1.0,2: 2.0, 3: 1.0,4: 1.0,5: 1.0}

sustabdymas = EarlyStopping(monitor='val_loss', patience=8, restore_best_weights=True)

# history = modelis.fit(
#     train_ds,
#     validation_data=val_ds,
#     epochs=70,
#     callbacks=[sustabdymas],
#     class_weight=klasiu_svoriai)

history = modelis.fit(train_ds,validation_data=val_ds,epochs=70,callbacks=[sustabdymas])

nuostolis, tikslumas = modelis.evaluate(test_ds, verbose=1)
print(f"Testo nuostolis: {nuostolis:.4f}")
print(f"Testo tikslumas: {tikslumas:.4f}")


y_tikros = np.concatenate([y for x, y in test_ds], axis=0)
y_spejimai = modelis.predict(test_ds)
y_spejamos = np.argmax(y_spejimai, axis=1)


conf_matrix = confusion_matrix(y_tikros, y_spejamos)
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=train_ds.class_names)
disp.plot(xticks_rotation=45, cmap='Blues')
plt.title("MobileNetV2 Matrica")
plt.tight_layout()
plt.show()


print(classification_report(y_tikros, y_spejamos, target_names=train_ds.class_names))

# modelis.save("mobilenet_modelis.h5")

