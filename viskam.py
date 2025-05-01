
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


train_kelias = r"C:\Users\Vartotojas\Desktop\POMIDORAI\pomidoru_duomenys\trenyravimas"
val_kelias = r"C:\Users\Vartotojas\Desktop\POMIDORAI\pomidoru_duomenys\validacija"
test_kelias = r"C:\Users\Vartotojas\Desktop\POMIDORAI\pomidoru_duomenys\testas"

train_df = tf.keras.utils.image_dataset_from_directory(train_kelias,image_size=(224, 224),batch_size=32)

val_df = tf.keras.utils.image_dataset_from_directory(val_kelias,image_size=(224, 224),batch_size=32)

test_df = tf.keras.utils.image_dataset_from_directory(test_kelias,image_size=(224, 224),batch_size=32)

# ---------------------------------------------------------

# class_names = train_df.class_names
# print(class_names)

# for images, labels in train_df.take(1):
#     plt.figure(figsize=(10, 10))
#     for i in range(9):
#         ax = plt.subplot(3, 3, i + 1)
#         plt.imshow(images[i].numpy().astype("uint8"))
#         plt.title(class_names[labels[i]])
#         plt.axis("off")
#         # plt.show()

# ----------------------------------------------------------------

# print(train_df.class_names)


# class_names = train_df.class_names

# for images, labels in train_df.take(1):
#     plt.figure(figsize=(10, 10))
#     for i in range(9):
#         ax = plt.subplot(3, 3, i + 1)
#         plt.imshow(images[i].numpy().astype("uint8"))  # <-- jei vaizdas ryškus, gerai
#         plt.title(class_names[labels[i]])
#         plt.axis("off")
#     plt.tight_layout()
#     plt.show()

# print("Vieno paveikslėlio forma:", images[0].shape)



# ---------------------------------------------------------------------

duomenu_augmentacija = keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
    layers.RandomContrast(0.1),])

augmentuota_train_df = train_df.map(lambda x, y: (duomenu_augmentacija(x, training = True),y),num_parallel_calls = tf.data.AUTOTUNE)




