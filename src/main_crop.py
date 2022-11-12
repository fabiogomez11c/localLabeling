from PIL import Image
import tensorflow as tf
import glob

# all files
images_files = glob.glob("src/downloads/*.png")
# images_files = glob.glob("images/*/*.png")


for idx, element in enumerate(images_files):
    # Opens a image in RGB mode
    tf.keras.preprocessing.image.load_img(element, target_size=(256, 256)).save(element)
    print(f'{len(images_files) - idx - 1} left.')

