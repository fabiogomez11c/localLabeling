import shutil
import glob
import tensorflow as tf
import numpy as np

if __name__ == '__main__':
  model = tf.keras.models.Sequential([
    tf.keras.layers.Rescaling(1./255, input_shape=(256, 256, 3)),
    tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(3042, activation='relu'),# activity_regularizer=tf.keras.regularizers.l2(REGULARIZATION_LAMBDA)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(2028, activation='relu'),# activity_regularizer=tf.keras.regularizers.l2(REGULARIZATION_LAMBDA)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(1014, activation='relu'),# activity_regularizer=tf.keras.regularizers.l2(REGULARIZATION_LAMBDA)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(512, activation='relu'),# activity_regularizer=tf.keras.regularizers.l2(REGULARIZATION_LAMBDA)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(256, activation='relu'),# activity_regularizer=tf.keras.regularizers.l2(REGULARIZATION_LAMBDA)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(128, activation='relu'),# activity_regularizer=tf.keras.regularizers.l2(REGULARIZATION_LAMBDA)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(64, activation='relu'),# activity_regularizer=tf.keras.regularizers.l2(REGULARIZATION_LAMBDA)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(1, activation='sigmoid')
  ])
  model.compile(
    loss='binary_crossentropy',
    metrics=['accuracy'],
  )
  model.load_weights('src/models/oi_model_w_v1.h5')
  labels = ['outside', 'inside']

  files = glob.glob('./src/downloads/*.png')
  # files_to_use = np.random.choice(files, 10000, replace=False)
  files_to_use = files

  # test model prediction
  for idx, image_filename in enumerate(files_to_use):
    name_file = image_filename.split('/')[-1]
    img = tf.keras.preprocessing.image.load_img(image_filename, target_size=(256, 256))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    pred = 1 - model.predict(img_array.reshape(1, 256, 256, 3))[0][0]
    thresholld = 0.9
    idx_pred = None
    if pred > thresholld:
      idx_pred = 0
    else:
      idx_pred = 1
    
    label_pred = labels[idx_pred]

    new_path = './src/images/' + label_pred + '/' + name_file

    # copy image to new folder
    shutil.move(image_filename, new_path)

    print(f'Image {image_filename} predicted as {label_pred}. {len(files_to_use) - idx} images left.')


