from PIL import Image
import numpy as np


#img = Image.open('newback.png')

#data = np.asarray(img, dtype=np.float)
data = np.full((576, 480, 4), 255)
data[:23, :, :] = [250,255,81, 255]
data[23, :, :] = [0, 0, 0, 255]
img = Image.fromarray(data.astype(np.int8), 'RGBA')
img.save('./img.png')