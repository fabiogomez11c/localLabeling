from PIL import Image
import glob

# all files
images_files = glob.glob("downloads/*.png")

for idx, element in enumerate(images_files):
    # Opens a image in RGB mode
    im = Image.open(element)

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
    im1.save('crop_images/' + str(idx) + '.png')

    print(f'{len(images_files) - idx - 1} left.')

