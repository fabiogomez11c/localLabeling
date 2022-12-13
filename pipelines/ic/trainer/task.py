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


# create and compile the model

# train the model



















