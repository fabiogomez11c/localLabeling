from PIL import Image
import imghdr
import glob

images_files = glob.glob("images/*/*.png")

image_extensions = [".png", ".jpg"]
img_type_accepted_by_tf = ["bmp", "gif", "jpeg", "png"]
for idx, img_file in enumerate(images_files):
  img_type = imghdr.what(img_file)
  if img_type is None:
      print(f"{img_file} is not an image")
  elif img_type not in img_type_accepted_by_tf:
      print(f"{img_file} is a {img_type}, not accepted by TensorFlow")
      im = Image.open(img_file).convert('RGB')
      im.save(img_file, 'png')
      print(f'Image done {img_file} - {len(images_files) - idx - 1} left.')

