import shutil
import glob
import tensorflow as tf
import numpy as np

if __name__ == '__main__':
  model = tf.keras.models.load_model('./src/labeling_model.h5')
  labels = ['back', 'front', 'other']

  files = glob.glob('./src/downloads2/*.png')

  # test model prediction
  for idx, image_filename in enumerate(files):
    name_file = image_filename.split('/')[-1]
    img = tf.keras.preprocessing.image.load_img(image_filename, target_size=(256, 256))
    img_array = tf.keras.preprocessing.image.img_to_array(img) / 255.0
    pred = model.predict(img_array.reshape(1, 256, 256, 3))
    label_pred = labels[np.argmax(pred)]

    new_path = './src/images/' + label_pred + '/' + name_file

    # copy image to new folder
    shutil.copy(image_filename, new_path)

    print(f'Image {image_filename} predicted as {label_pred}. {len(files) - idx} images left.')


