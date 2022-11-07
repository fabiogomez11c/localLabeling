from PIL import Image
import glob

images_files = glob.glob("images/*/*.png")

for idx, img_file in enumerate(images_files):
  # print(img_file)
  im = Image.open(img_file).convert('RGB')
  im.save(img_file, 'png')
  print(f'Image done {img_file} - {len(images_files) - idx - 1} left.')

