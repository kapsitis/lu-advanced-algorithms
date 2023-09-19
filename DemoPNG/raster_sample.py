from PIL import Image
import numpy as np

# 100x100 nejauši reāli skaitļi intervālā [0;1]
imageArray = np.random.rand(100,100)
# Izmaina mērogu uz [0;255] melnbaltā attēlā "255" ir balts
img = Image.fromarray(imageArray * 255)
# Eksportē uz PNG failu
img.convert('RGB').save('raster_output.png')
