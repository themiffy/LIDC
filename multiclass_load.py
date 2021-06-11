import tensorflow as tf
import os
import numpy as np
from skimage.io import imread, imshow
from skimage.transform import resize
from skimage import color
import matplotlib.pyplot as plt
import glob

img_width = 256
img_height = 256

train_path = 'single/train/'
test_path = 'single/test/'
 
trainFileNames = glob.glob(train_path + 'images/*')
 
X_train = np.zeros((len(trainFileNames), img_width, img_height), dtype = np.float)
Y_train = np.zeros((len(trainFileNames), img_width, img_height), dtype = np.bool)
masks = np.zeros((len(trainFileNames),5 , img_width, img_height), dtype = np.bool)

n = 0
for file in glob.glob(train_path + 'images/*'):
 
    img = color.rgb2gray(imread(file))
    #resize if needed
    img = resize(img, (img_height, img_width), mode='constant', preserve_range=True)
    X_train[n] = img
 
    #mask = imread(file[0:36]+ 'masks/rtop/'+ file[43:53]+ '_Rhigh.ome.tiff') # for google drive
    rtop = imread(file[0:13]+ 'masks/rtop/'+ file[20:30]+ '_Rhigh.ome.tiff', as_gray=True)
    rtop = resize(rtop, (img_height, img_width), mode='constant', preserve_range=True)
    masks[n][0] = rtop

    rmid = imread(file[0:13]+ 'masks/rmid/'+ file[20:30]+ '_Rmid.ome.tiff', as_gray=True)
    rmid = resize(rmid, (img_height, img_width), mode='constant', preserve_range=True)
    masks[n][1] = rmid

    rbot = imread(file[0:13]+ 'masks/rbot/'+ file[20:30]+ '_Rlow.ome.tiff', as_gray=True)
    rbot = resize(rbot, (img_height, img_width), mode='constant', preserve_range=True)
    masks[n][2] = rbot

    ltop = imread(file[0:13]+ 'masks/ltop/'+ file[20:30]+ '_Lhigh.ome.tiff', as_gray=True)
    ltop = resize(ltop, (img_height, img_width), mode='constant', preserve_range=True)
    masks[n][3] = ltop

    lbot = imread(file[0:13]+ 'masks/lbot/'+ file[20:30]+ '_Llow.ome.tiff', as_gray=True)
    lbot = resize(lbot, (img_height, img_width), mode='constant', preserve_range=True)
    masks[n][4] = lbot

    #Y_train[n] = mask
    n+=1

ix = 4
f, axarr = plt.subplots(1,5) 

axarr[0].imshow(masks[ix][0])
axarr[1].imshow(masks[ix][1])
axarr[2].imshow(masks[ix][2])
axarr[3].imshow(masks[ix][3])
axarr[4].imshow(masks[ix][4])
plt.show()