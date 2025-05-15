from skimage.feature import hog
from skimage.color import rgb2gray
import numpy as np

def istraukti_hog(paveiksleliai):
    hog_pozymiai = []
    for paveikslelis in paveiksleliai:
        pilkas_normalizuotas = rgb2gray(paveikslelis / 255.0) 
        pozymiai = hog(
            pilkas_normalizuotas,
            pixels_per_cell=(16, 16),
            cells_per_block=(3, 3),
            orientations=9,
            feature_vector=True)
        hog_pozymiai.append(pozymiai)
    return np.array(hog_pozymiai)