from PIL import Image
import glob

# all files
# images_files = glob.glob("downloads/*.png")
images_files = glob.glob("downloads/*.png")

for idx, element in enumerate(images_files):
    # Opens a image in RGB mode
    im = Image.open(element)
    im_name = element.split('/')[-1]

    # Size of the image in pixels (size of original image)
    # (This is not mandatory)
    width, height = im.size

    # Setting the points for cropped image
    left = width * 0.1
    top = height * 0.1
    right = width * 0.9
    bottom = height * 0.9

    # Cropped image of above dimension
    im1 = im.crop((left, top, right, bottom))
    im1.save('crop_images/' + im_name)

    print(f'{len(images_files) - idx - 1} left.')

