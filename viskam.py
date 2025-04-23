from tensorflow.keras.preprocessing import image_dataset_from_directory

train_df = image_dataset_from_directory(r"C:\Users\Vartotojas\Desktop\POMIDORAI\archive (1)\plantvillage",validation_split = 0.2,
                                        subset="training",seed=42,image_size = (224,224), batch_size=32)

validation_df = image_dataset_from_directory(r"C:\Users\Vartotojas\Desktop\POMIDORAI\archive (1)\plantvillage",validation_split = 0.2,
                                        subset="validation",seed=42,image_size = (224,224), batch_size=32 )