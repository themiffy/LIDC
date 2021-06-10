import tensorflow as tf
import os
import numpy as np
from skimage.io import imread, imshow
from skimage.transform import resize
from skimage import color
import matplotlib.pyplot as plt
import glob

################### model parameters
 
img_width = 256
img_height = 256
img_channels = 1
start_neurons = 16 #(16 - starts to decrease at 60 epoch and should go over 70)
 
dropout = 0.01
 
################### data path

#train_path = '/content/drive/MyDrive/single/train/'
#test_path = '/content/drive/MyDrive/single/test/'

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

print(len(trainFileNames))
plt.imshow(X_train[5])
plt.show()
plt.imshow(Y_train[5])
plt.show()
#model = tf.keras.models.load_model('/content/drive/MyDrive/single/model-1')

#model
 
inputs = tf.keras.layers.Input((img_width, img_height, img_channels))
s = tf.keras.layers.Lambda(lambda x: x / 255)(inputs)
 
c1 = tf.keras.layers.Conv2D(start_neurons, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(s)
c1 = tf.keras.layers.Dropout(dropout)(c1)
c1 = tf.keras.layers.Conv2D(start_neurons, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c1)
p1 = tf.keras.layers.MaxPooling2D((2, 2))(c1)
 
c2 = tf.keras.layers.Conv2D(start_neurons*2, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p1)
c2 = tf.keras.layers.Dropout(dropout)(c2)
c2 = tf.keras.layers.Conv2D(start_neurons*2, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c2)
p2 = tf.keras.layers.MaxPooling2D((2, 2))(c2)
 
c3 = tf.keras.layers.Conv2D(start_neurons*4, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p2)
c3 = tf.keras.layers.Dropout(dropout + 0.1)(c3)
c3 = tf.keras.layers.Conv2D(start_neurons*4, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c3)
p3 = tf.keras.layers.MaxPooling2D((2, 2))(c3)
 
c4 = tf.keras.layers.Conv2D(start_neurons*8, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p3)
c4 = tf.keras.layers.Dropout(dropout + 0.1)(c4)
c4 = tf.keras.layers.Conv2D(start_neurons*8, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c4)
p4 = tf.keras.layers.MaxPooling2D(pool_size=(2, 2))(c4)
 
c5 = tf.keras.layers.Conv2D(start_neurons*16, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(p4)
c5 = tf.keras.layers.Dropout(dropout + 0.2)(c5)
c5 = tf.keras.layers.Conv2D(start_neurons*16, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c5)
 
################### expansive path 

u6 = tf.keras.layers.Conv2DTranspose(start_neurons*8, (2, 2), strides=(2, 2), padding='same')(c5)
u6 = tf.keras.layers.concatenate([u6, c4])
c6 = tf.keras.layers.Conv2D(start_neurons*8, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u6)
c6 = tf.keras.layers.Dropout(dropout + 0.1)(c6)
c6 = tf.keras.layers.Conv2D(start_neurons*8, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c6)
 
u7 = tf.keras.layers.Conv2DTranspose(start_neurons*4, (2, 2), strides=(2, 2), padding='same')(c6)
u7 = tf.keras.layers.concatenate([u7, c3])
c7 = tf.keras.layers.Conv2D(start_neurons*4, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u7)
c7 = tf.keras.layers.Dropout(dropout + 0.1)(c7)
c7 = tf.keras.layers.Conv2D(start_neurons*4, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c7)
 
u8 = tf.keras.layers.Conv2DTranspose(start_neurons*2, (2, 2), strides=(2, 2), padding='same')(c7)
u8 = tf.keras.layers.concatenate([u8, c2])
c8 = tf.keras.layers.Conv2D(start_neurons*2, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u8)
c8 = tf.keras.layers.Dropout(dropout)(c8)
c8 = tf.keras.layers.Conv2D(start_neurons*2, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c8)
 
u9 = tf.keras.layers.Conv2DTranspose(start_neurons, (2, 2), strides=(2, 2), padding='same')(c8)
u9 = tf.keras.layers.concatenate([u9, c1], axis=3)
c9 = tf.keras.layers.Conv2D(start_neurons, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(u9)
c9 = tf.keras.layers.Dropout(dropout)(c9)
c9 = tf.keras.layers.Conv2D(start_neurons, (3, 3), activation='relu', kernel_initializer='he_normal', padding='same')(c9)
 
outputs = tf.keras.layers.Conv2D(1, (1, 1), activation='sigmoid')(c9)
 
model = tf.keras.Model(inputs = [inputs], outputs = [outputs])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
#model.summary()
 
#Checkpoints
checkpointer = tf.keras.callbacks.ModelCheckpoint('best.h5', verbose = 1, save_best_only = True)
 
#Callbacks
callbacks = [
             #tf.keras.callbacks.EarlyStopping(patience=2, monitor='val_loss'), #stop if there's no progress
             tf.keras.callbacks.TensorBoard(log_dir='logs')] #make logs

################### train model

results = model.fit(X_train,
                    Y_train,
                    validation_split = 0.2,
                    batch_size = 12,
                    epochs=70,
                    callbacks=callbacks)

#model.save('test')

preds_train = model.predict(X_train[:int(X_train.shape[0]*0.9)], verbose=1)
preds_val = model.predict(X_train[int(X_train.shape[0]*0.9):], verbose=1)
preds_test = model.predict(X_test, verbose=1)

ix = 1

f, axarr = plt.subplots(1,3) 

axarr[0].imshow(X_train[ix])
axarr[1].imshow(np.squeeze(Y_train[ix]))
axarr[2].imshow(np.squeeze(preds_train[ix]))

plt.show()