
import matplotlib.pyplot as plt
import tensorflow as tf


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

