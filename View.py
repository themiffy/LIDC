import tensorflow as tf
import numpy as np
from skimage.io import imread, imshow
from skimage.transform import resize
from skimage import color
import matplotlib.pyplot as plt
import glob

img_width = 256
img_height = 256
img_channels = 1
start_neurons = 8
 
dropout = 0.01

train_path = 'single/train/'
test_path = 'single/test/'
 
trainFileNames = glob.glob(train_path + 'images/*')
testFileNames = glob.glob(test_path + '*')
  
X_train = np.zeros((len(trainFileNames), img_width, img_height), dtype = np.float)
Y_train = np.zeros((len(trainFileNames), img_width, img_height), dtype = np.bool)
X_test = np.zeros((len(testFileNames), img_height, img_width), dtype = np.float)

################### load images

n = 0
for file in glob.glob(train_path + 'images/*'):
 
    img = color.rgb2gray(imread(file))
    #resize if needed
    img = resize(img, (img_height, img_width), mode='constant', preserve_range=True)
    X_train[n] = img
 
    #mask = imread(file[0:36]+ 'masks/rtop/'+ file[43:53]+ '_Rhigh.ome.tiff') # for google drive
    mask = imread(file[0:13]+ 'masks/rtop/'+ file[20:30]+ '_Rhigh.ome.tiff', as_gray=True)
    mask = resize(mask, (img_height, img_width), mode='constant', preserve_range=True)
    Y_train[n] = mask
    n+=1

n = 0
for file in glob.glob(test_path + '*'):
    img = color.rgb2gray(imread(file))
    #resize if needed
    img = resize(img, (img_height, img_width), mode='constant', preserve_range=True)
    X_test[n] = img
    n+=1


model = tf.keras.models.load_model('test')

#preds_train = model.predict(X_train[:int(X_train.shape[0]*0.9)], verbose=1)
#preds_val = model.predict(X_train[int(X_train.shape[0]*0.9):], verbose=1)
preds_test = model.predict(X_test, verbose=1)

ix = 4
#plt.figure()
f, axarr = plt.subplots(1,3) 

axarr[0].imshow(X_test[ix])
#axarr[1].imshow(np.squeeze(Y_test[ix]))
axarr[2].imshow(np.squeeze(preds_test[ix]))
plt.show()