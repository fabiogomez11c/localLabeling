
import logging

from google.cloud import storage
import tensorflow as tf
from flask import jsonify

IMG_WIDTH = 128

def download_blob(bucket_name, source_blob_name, destination_file_name):
  """Downloads a blob from the bucket."""
  # The ID of your GCS bucket
  # bucket_name = "your-bucket-name"

  # The ID of your GCS object
  # source_blob_name = "storage-object-name"

  # The path to which the file should be downloaded
  # destination_file_name = "local/path/to/file"

  storage_client = storage.Client()

  bucket = storage_client.bucket(bucket_name)

  # Construct a client side representation of a blob.
  # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
  # any content from Google Cloud Storage. As we don't need additional data,
  # using `Bucket.blob` is preferred here.
  blob = bucket.blob(source_blob_name)
  blob.download_to_filename(destination_file_name)

  logging.info(
    "Downloaded storage object {} from bucket {} to local file {}.".format(
      source_blob_name, bucket_name, destination_file_name
    )
  )

def preprocess_image():
  # download the image
  download_blob('mom_seguros_images_car/ic/train/train/correct', '0.9548_car_a5fcb34e-68db-11ed-b6d3-ce59abab15a2.png', './0.9548_car_a5fcb34e-68db-11ed-b6d3-ce59abab15a2.png')

  # preprocess the image
  image_filepath = './0.9548_car_a5fcb34e-68db-11ed-b6d3-ce59abab15a2.png'
  image = tf.keras.utils.load_img(image_filepath, target_size=(IMG_WIDTH, IMG_WIDTH))
  image_array = tf.keras.utils.img_to_array(image)
  return image_array.reshape(1, IMG_WIDTH, IMG_WIDTH, 3)

def load_model():
  download_blob('mom_seguros_images_car', 'gcf_model.h5', './gcf_model.h5')
  new_model = tf.keras.models.load_model('gcf_model.h5')
  return new_model

def classify_ic(request):
  # Set CORS headers for the preflight request
  # if request.method == 'OPTIONS':
  #   # Allows POST requests from any origin with the Content-Type
  #   # header and caches preflight response for an 3600s
  #   headers = {
  #     'Access-Control-Allow-Origin': '*',
  #     'Access-Control-Allow-Methods': 'POST',
  #     'Access-Control-Allow-Headers': 'Content-Type',
  #     'Access-Control-Max-Age': '3600'
  #   }
  #   return ('', 204, headers)

  # # Disallow non-POSTs
  # if request.method != 'POST':
  #   return ('Not found', 404)

  # Set CORS headers for the main request
  headers = {'Access-Control-Allow-Origin': '*'}

  # request_json = request.get_json(silent=True)
  # if not request_json or not 'image_url' in request_json:
  #   return ('Invalid request', 400, headers)

  # instance = preprocess_image(request_json['image_url'])
  model = load_model()
  image = preprocess_image()
  # if not instance:
  #   return ('Invalid request', 400, headers)

  raw_prediction = model.predict(image)[0][0]
  # if not raw_prediction:
  #   return ('Error getting prediction', 500, headers)
  return (jsonify({'prediction:': raw_prediction}), 200, headers)







