import numpy as np
from skimage.io import imread, imshow
from skimage.transform import resize
from skimage import color
import matplotlib.pyplot as plt
import glob

def load_data(img_width = 256, img_height = 256, path = 'single/train/', test = False):

    # Function that loads multiclass data from my folder and returns X_train and Y_train arrays

    file_names = glob.glob(path + 'images/*')
    X_train = np.zeros((len(file_names), img_width, img_height), dtype = np.float)
    temp_array = np.zeros((len(file_names),5 , img_width, img_height), dtype = np.int) # an array used for some dirty sorcery
    Y_train = np.zeros((len(file_names), img_width, img_height), dtype = np.int)
    n = 0

    for file in glob.glob(path + 'images/*'):
        # Load image
        img = color.rgb2gray(imread(file)) # convert to grayscale
        img = resize(img, (img_height, img_width), mode='constant', preserve_range=True)
        X_train[n] = img

        # Load masks
        if not test:
          rtop = imread(file[0:13]+ 'masks/'+ file[20:30]+ '_Rhigh.ome.tiff', as_gray=True)
          rtop = resize(rtop, (img_height, img_width), mode='constant', preserve_range=True)
          temp_array[n][0] = rtop # temp_array is used to contain images and automaticaly convert to integer
          # value for first class is already "1"

          rmid = imread(file[0:13]+ 'masks/'+ file[20:30]+ '_Rmid.ome.tiff', as_gray=True)
          rmid = resize(rmid, (img_height, img_width), mode='constant', preserve_range=True)
          temp_array[n][1] = rmid
          temp_array[n][1][temp_array[n][1] == 1] = 2 # changing every "1" with "2" so pixels for second class are "2"
          Y_train[n] = np.bitwise_or(temp_array[n][0],temp_array[n][1]) # adding two masks together

          rbot = imread(file[0:13]+ 'masks/'+ file[20:30]+ '_Rlow.ome.tiff', as_gray=True)
          rbot = resize(rbot, (img_height, img_width), mode='constant', preserve_range=True)
          temp_array[n][2] = rbot
          temp_array[n][2][temp_array[n][2] == 1] = 3
          Y_train[n] = np.bitwise_or(Y_train[n],temp_array[n][2]) # adding previous mask with new one

          ltop = imread(file[0:13]+ 'masks/'+ file[20:30]+ '_Lhigh.ome.tiff', as_gray=True)
          ltop = resize(ltop, (img_height, img_width), mode='constant', preserve_range=True)
          temp_array[n][3] = ltop
          temp_array[n][3][temp_array[n][3] == 1] = 4
          Y_train[n] = np.bitwise_or(Y_train[n],temp_array[n][3])

          lbot = imread(file[0:13]+ 'masks/'+ file[20:30]+ '_Llow.ome.tiff', as_gray=True)
          lbot = resize(lbot, (img_height, img_width), mode='constant', preserve_range=True)
          temp_array[n][4] = lbot
          temp_array[n][4][temp_array[n][4] == 1] = 5

          Y_train[n] = np.bitwise_or(Y_train[n],temp_array[n][4]) # finally sum it all up
        n+=1

    if not test:
      return X_train, Y_train
    else:
      return X_train

image, mask = load_data(path = 'datset/train/')

for ix in range(0, 68):

  f, axarr = plt.subplots(1,2) 

  axarr[0].imshow(image[ix])
  axarr[1].imshow(mask[ix])
  plt.show()
