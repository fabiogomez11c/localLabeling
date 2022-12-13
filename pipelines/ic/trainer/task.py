import logging
import tensorflow as tf

from get_images import download_images

BATCH_SIZE = 32
IMAGE_SIZE = (256, 256)
CLASS_NAMES = ['incorrect', 'correct']

logging.info(f'List GPUs: {tf.config.list_physical_devices("GPU")}')

# get images
logging.info('Downloading images')
download_images('gs://mom_seguros_images_car/ic/', 'ic/')

# create the dataset
logging.info(f'Creating datasets for training')
train_ds = tf.keras.utils.image_dataset_from_directory(
  'ic/train',
  class_names=CLASS_NAMES,
  seed=123,
  image_size=IMAGE_SIZE,
  batch_size=BATCH_SIZE
)
val_ds = tf.keras.utils.image_dataset_from_directory(
  'ic/validation',
  class_names=CLASS_NAMES,
  shuffle=False,
  image_size=IMAGE_SIZE,
  batch_size=BATCH_SIZE
)
test_ds = tf.keras.utils.image_dataset_from_directory(
  'ic/test',
  class_names=CLASS_NAMES,
  shuffle=False,
  image_size=IMAGE_SIZE,
  batch_size=BATCH_SIZE
)     

# create and compile the model

# train the model



















