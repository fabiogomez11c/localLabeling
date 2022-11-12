import shutil
import glob
import tensorflow as tf
import numpy as np

if __name__ == '__main__':
  model = tf.keras.models.load_model('./src/labeling_model_ic.h5')
  labels = ['other', 'correct']

  files = glob.glob('./src/downloads/*.png')
  # files_to_use = np.random.choice(files, 10000, replace=False)
  files_to_use = files

  # test model prediction
  for idx, image_filename in enumerate(files_to_use):
    name_file = image_filename.split('/')[-1]
    img = tf.keras.preprocessing.image.load_img(image_filename, target_size=(256, 256))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    pred = model.predict(img_array.reshape(1, 256, 256, 3))
    thresholld = 0.95
    idx_pred = None
    if pred > thresholld:
      idx_pred = 1
    else:
      idx_pred = 0
    
    label_pred = labels[idx_pred]

    new_path = './src/images/' + label_pred + '/' + name_file

    # copy image to new folder
    shutil.move(image_filename, new_path)

    print(f'Image {image_filename} predicted as {label_pred}. {len(files_to_use) - idx} images left.')


