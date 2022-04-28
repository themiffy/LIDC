import pydicom as dicom
import os
import matplotlib.pyplot as plt
import sys
import glob
import numpy as np


slices = dicom.dcmread('LUNG_SPECT_CT/DICOM/17102719/25530000/77306389')

print(slices.pixel_array.shape)

fig = plt.figure()

# pixel aspects, assuming all slices are the same
ps = slices.PixelSpacing
ss = slices.SliceThickness
ax_aspect = ps[1]/ps[0]
sag_aspect = ps[1]/ss
cor_aspect = ss/ps[0]

# create 3D array
img_shape = list(slices.pixel_array[0].shape)
img_shape.append(len(slices.pixel_array))
img3d = np.zeros(img_shape)

# fill 3D array with the images from the files
for i, s in enumerate(slices.pixel_array):
    img2d = s
    img3d[:, :, i] = img2d

print(img3d.shape)
# plot 3 orthogonal slices
a1 = plt.subplot(2, 2, 1)
plt.imshow(img3d[:, :, img_shape[2]//2])
a1.set_aspect(ax_aspect)

a2 = plt.subplot(2, 2, 2)
plt.imshow(img3d[:, img_shape[1]//2, :])
a2.set_aspect(sag_aspect)

a3 = plt.subplot(2, 2, 3)
plt.imshow(img3d[img_shape[0]//2, :, :].T)
a3.set_aspect(cor_aspect)

plt.show()
