import logging
import os
import tensorflow as tf
from subprocess import run

# Global parameters
BATCH_SIZE = 32
IMAGE_SIZE = (128, 128)
CLASS_NAMES = ['incorrect', 'correct']
AUTOTUNE = tf.data.AUTOTUNE
REGULARIZATION_LAMBDA = 0.000025
FILENAMES = "gs://mom_seguros_poc/images/ic/train/*/*.png"
FILENAMES_VAL = "gs://mom_seguros_poc/images/ic/validation/*/*.png"

output_directory = os.environ['AIP_MODEL_DIR']

# List all files in bucket
filepath = tf.io.gfile.glob(FILENAMES)
filepath_val = tf.io.gfile.glob(FILENAMES_VAL)
NUM_TOTAL_IMAGES = len(filepath)

def assign_label(label_map: dict, filepath: list) -> dict:
  """
  Creates a dict with labels for training.
  """
  labels = dict()

  for i in range(len(filepath)):
    label = filepath[i].split('/')[-2]
    if label not in list(label_map.keys()):
      raise NotImplementedError(f'Label {label} not included in label map')
      
    labels.update({filepath[i]:label_map[label]})

  return labels

def get_bytes_label(filepath, label):
    raw_bytes = tf.io.read_file(filepath)
    return raw_bytes, label

def process_image(raw_bytes, label):
    image = tf.io.decode_png(raw_bytes, channels=3)
    image = tf.image.convert_image_dtype(image, dtype=tf.float32)
    image = tf.image.resize(image, (128, 128)) # needed in order to have correct shape otherwise it gets None shape in training
    
    return image, label

def build_dataset(dataset, batch_size=BATCH_SIZE, cache=False, shuffle=True):
    
    if shuffle:
      dataset = dataset.shuffle(NUM_TOTAL_IMAGES)
    
    # Extraction: IO Intensive
    dataset = dataset.map(get_bytes_label, num_parallel_calls=AUTOTUNE)

    # Transformation: CPU Intensive
    dataset = dataset.map(process_image, num_parallel_calls=AUTOTUNE)
    # dataset = dataset.repeat()
    dataset = dataset.batch(batch_size=batch_size)
    
    if cache:
        if isinstance(cache, str):
            dataset = dataset.cache(filename=cache)
        else:
            dataset = dataset.cache()
    
    # Pipeline next iteration
    dataset = dataset.prefetch(buffer_size=AUTOTUNE)
    
    return dataset

logging.info(f'List GPUs: {tf.config.list_physical_devices("GPU")}')

# get images
logging.info('Images pipeline starting')
logging.info('Creating dataset with gcs paths')
label_map = {'correct': 1, 'incorrect': 0}
dataset = assign_label(label_map, filepath)
val_dataset = assign_label(label_map, filepath_val)
dataset = [[k,v] for k,v in dataset.items()]
val_dataset = [[k,v] for k,v in val_dataset.items()]

features = [i[0] for i in dataset]
labels = [i[1] for i in dataset]
val_features = [i[0] for i in val_dataset]
val_labels = [i[1] for i in val_dataset]

# Create Dataset from Features and Labels
dataset = tf.data.Dataset.from_tensor_slices((features, labels))
val_dataset = tf.data.Dataset.from_tensor_slices((val_features, val_labels))

logging.info(f'Creating datasets for training')
# Apply transformations to the dataset with images paths and labels
train_ds = build_dataset(dataset)
val_ds = build_dataset(val_dataset, shuffle=False)

# data augmentation layer
data_augmentation = tf.keras.Sequential([
  tf.keras.layers.RandomFlip("horizontal_and_vertical"),
  tf.keras.layers.RandomRotation(0.2),
])

# create and compile the model
logging.info('Creating and compiling the model')
# callbacks
class AccReached(tf.keras.callbacks.Callback):
  def __init__(self):
    pass
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('accuracy') > 0.999):
      print("\nReached 99% accuracy so cancelling training!")
      self.model.stop_training = True

def scheduler(epoch, lr):
  if epoch < 10:
    return lr
  elif lr <= 0.003:
    return lr * tf.math.exp(-0.01)
  else:
    return lr * tf.math.exp(-0.1)

lr_callback = tf.keras.callbacks.LearningRateScheduler(scheduler)

model = tf.keras.Sequential([
  data_augmentation,
  tf.keras.layers.Rescaling(1./255, input_shape=(256, 256, 3)),
  tf.keras.layers.Conv2D(32, (4,4), activation='relu'),
  tf.keras.layers.MaxPooling2D(2,2),
  tf.keras.layers.Conv2D(32, (4,4), activation='relu'),
  tf.keras.layers.MaxPooling2D(2,2),
  tf.keras.layers.Conv2D(64, (4,4), activation='relu'),
  tf.keras.layers.MaxPooling2D(2,2),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(2048, activation='relu', activity_regularizer=tf.keras.regularizers.l2(REGULARIZATION_LAMBDA)),
  tf.keras.layers.Dense(1024, activation='relu', activity_regularizer=tf.keras.regularizers.l2(REGULARIZATION_LAMBDA)),
  tf.keras.layers.Dense(1024, activation='relu', activity_regularizer=tf.keras.regularizers.l2(REGULARIZATION_LAMBDA)),
  tf.keras.layers.Dense(1024, activation='relu', activity_regularizer=tf.keras.regularizers.l2(REGULARIZATION_LAMBDA)),
  tf.keras.layers.Dense(1024, activation='relu', activity_regularizer=tf.keras.regularizers.l2(REGULARIZATION_LAMBDA)),
  tf.keras.layers.Dense(1024, activation='relu', activity_regularizer=tf.keras.regularizers.l2(REGULARIZATION_LAMBDA)),
  tf.keras.layers.Dense(1024, activation='relu', activity_regularizer=tf.keras.regularizers.l2(REGULARIZATION_LAMBDA)),
  tf.keras.layers.Dense(1024, activation='relu', activity_regularizer=tf.keras.regularizers.l2(REGULARIZATION_LAMBDA)),
  tf.keras.layers.Dense(1024, activation='relu', activity_regularizer=tf.keras.regularizers.l2(REGULARIZATION_LAMBDA)),
  tf.keras.layers.Dense(1024, activation='relu', activity_regularizer=tf.keras.regularizers.l2(REGULARIZATION_LAMBDA)),
  tf.keras.layers.Dense(512, activation='relu', activity_regularizer=tf.keras.regularizers.l2(REGULARIZATION_LAMBDA)),
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
  callbacks=[lr_callback, AccReached()],
  validation_data=val_ds,
)

# model save
model.save(output_directory)


















