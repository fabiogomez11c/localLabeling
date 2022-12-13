import logging
from google.cloud import storage
from subprocess import run

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
    print('Downloading . . .')
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)
    print(
        "Downloaded storage object {} from bucket {} to local file {}.".format(
            source_blob_name, bucket_name, destination_file_name
        )
    )

def download_images(copy_from_path, copy_to_path):
    """
    Copy folder from one path to another path, it uses gsutil cli.
    """
    return_obj = run(['gsutil', '-m', 'cp', '-r', copy_from_path, copy_to_path])
    if return_obj.returncode == 0:
        logging.info('Images downloaded correctly')
    else:
        logging.error('Error dowloading images')