import logging
import os
import tensorflow as tf

from get_images import download_images

BATCH_SIZE = 32
IMAGE_SIZE = (256, 256)
CLASS_NAMES = ['incorrect', 'correct']
AUTOTUNE = tf.data.AUTOTUNE
REGULARIZATION_LAMBDA = 0.000025

output_directory = os.environ['API_MODEL_DIR']

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
# data augmentation layer
data_augmentation = tf.keras.Sequential([
  tf.keras.layers.RandomFlip("horizontal_and_vertical"),
  tf.keras.layers.RandomRotation(0.2),
])

train_ds = train_ds.prefetch(AUTOTUNE)
val_ds = val_ds.prefetch(AUTOTUNE)

# create and compile the model
logging.info('Creating and compiling the model')
model = tf.keras.Sequential([
  tf.keras.layers.Rescaling(1./255, input_shape=(256, 256, 3)),
  tf.keras.layers.Dense(64, activation='relu', activity_regularizer=tf.keras.regularizers.l2(REGULARIZATION_LAMBDA)),
  tf.keras.layers.Dense(1, activation='sigmoid')
])
model.compile(
  loss='binary_crossentropy',
  optimizer=tf.optimizers.SGD(learning_rate=0.01),
  metrics=['accuracy'],
)

# train the model
model.fit(
  train_ds,
  epochs=5,
  verbose=1,
  validation_data=val_ds,
)

# model save
model.save(output_directory)


















