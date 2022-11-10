import shutil
import glob
import tensorflow as tf
import numpy as np

if __name__ == '__main__':
  model = tf.keras.models.load_model('./src/labeling_model.h5')
  labels = ['back', 'front', 'other']

  files = glob.glob('./src/downloads/*.png')
  files_to_use = np.random.choice(files, 4000, replace=False)

  # test model prediction
  for idx, image_filename in enumerate(files_to_use):
    name_file = image_filename.split('/')[-1]
    img = tf.keras.preprocessing.image.load_img(image_filename, target_size=(256, 256))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    pred = model.predict(img_array.reshape(1, 256, 256, 3))
    thresholld = 0.7
    idx_pred = None
    if pred[0] > thresholld:
      idx_pred = 0
    elif pred[1] > thresholld:
      idx_pred = 1
    else:
      idx_pred = 2
    
    label_pred = labels[np.argmax(pred)]

    new_path = './src/images/' + label_pred + '/' + name_file

    # copy image to new folder
    shutil.move(image_filename, new_path)

    print(f'Image {image_filename} predicted as {label_pred}. {len(files_to_use) - idx} images left.')


