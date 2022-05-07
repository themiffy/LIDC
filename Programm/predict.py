import tensorflow as tf
from skimage.io import imread # input 
from skimage.transform import resize 
from skimage import color 
from utilities import window_ct
import numpy as np

model = tf.keras.models.load_model("model200.h5")


def make_prediction(image, img_height = 256, img_width = 256): # OLD!!!!!!!!!!!!!!!!!!
    #img = color.rgb2gray(imread(image)) # convert to grayscale
    img = color.rgb2gray(image) # convert to grayscale
    img = resize(img, (img_height, img_width), mode='constant', preserve_range=True)
    images = np.zeros((1, img_width, img_height), dtype = np.float) # empty array for one picture. It doesnt work other way
    images[0] = img
    pred_argmax=np.argmax(model.predict(images), axis=3)

    return pred_argmax[0], images[0]

def segment(CT, orient, window_center = -400, window_width = 1500):
    if orient == 'coronal':
        windowed_slices = [window_ct(sl, window_width, window_center, 0, 1, meta = CT.meta) for sl in CT.coronal]
        np_slices = np.array(windowed_slices)
        import matplotlib.pyplot as plt
        plt.imshow(np_slices[50])
        plt.show()
        pred_argmax = np.argmax(model.predict(np_slices), axis=3)
        return pred_argmax