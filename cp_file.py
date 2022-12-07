# copy images from one folder to another

import glob
import shutil
import numpy as np

# source folder
src = './images/oi/train/outside/'
destination = './images/oi/borrar/'

# list all files in the source folder
files_to_copy = np.random.choice(np.array(glob.glob(src + '*.png')), 1000, replace=False)
for file in files_to_copy:
    shutil.move(file, destination)

