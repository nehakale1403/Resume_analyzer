# from tensorflow.keras.preprocessing.image import ImageDataGenerator
# from tensorflow.keras import applications
# from efficientnet.tfkeras import EfficientNetB0 #EfficientNetB1, EfficientNetB2, EfficientNetB3, EfficientNetB4, EfficientNetB5, EfficientNetB6, EfficientNetB7
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, Dropout
# from tensorflow.keras.optimizers import Adam
# from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
# from tensorflow.keras.models import load_model
# import pandas as pd

# new_model = load_model('./models/best_model.h5')

# print(new_model.summary())

# test_datagen1 = ImageDataGenerator(
#         rescale = 1/255  
#     )

# test_generator1 = test_datagen1.flow_from_directory(
#         directory = './images/',
#         classes=['img'],
#         target_size = (128, 128),
#         color_mode = "rgb",
#         class_mode = None,
#         batch_size = 1,
#         shuffle = False
#     )

# test_generator1.reset()

# preds = new_model.predict(
#         test_generator1,
#         verbose = 1
# )

# test_results = pd.DataFrame({
#         "Filename": test_generator1.filenames,
#         "Prediction": preds.flatten()
# })  

# print(test_results['Prediction'][0])

import os

folder_path = (r'./images/img/')

test = os.listdir(folder_path)
for images in test:
        if images.endswith(".jpg"):
                os.remove(os.path.join(folder_path, images))