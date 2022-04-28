import tensorflow as tf
from skimage.io import imread # input 
from skimage.transform import resize 
from skimage import color 
import numpy as np

model = tf.keras.models.load_model("model200.h5")


def make_prediction(image, img_height = 256, img_width = 256):
    img = color.rgb2gray(imread(image)) # convert to grayscale
    img = resize(img, (img_height, img_width), mode='constant', preserve_range=True)
    images = np.zeros((1, img_width, img_height), dtype = np.float) # empty array for one picture. It doesnt work other way
    images[0] = img
    pred_argmax=np.argmax(model.predict(images), axis=3)

    return pred_argmax[0], images[0]


