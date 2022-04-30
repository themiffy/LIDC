import numpy as np

class DicomVolumeCT():
    def __init__(self, pixel_array, meta):
        self.meta = meta
        self.pixel_array = pixel_array

        # pixel aspects, assuming all slices are the same
        self.coronal_aspect = meta.SliceThickness/meta.PixelSpacing[0]
        self.sagittal_aspect = meta.PixelSpacing[1]/meta.SliceThickness * 16
        self.axial_aspect = meta.PixelSpacing[1]/meta.PixelSpacing[0]

        # create 3D array
        self.img_shape = list(pixel_array[0].shape)
        self.img_shape.append(len(pixel_array))
        self.volume = np.zeros(self.img_shape)

        # fill 3D array with the images from the files
        for i, slice in enumerate(pixel_array):
            self.volume[:, :, i] = slice
        
        self.coronal = []
        self.axial = []
        self.sagittal = []
        for i, slice in enumerate(self.volume):
            self.coronal.append(self.volume[i,:,:].T)
            self.sagittal.append(self.volume[:,i,:])
            if i < self.volume.shape[2]:
                self.axial.append(self.volume[:,:,i])

        self.sagittal = np.rot90(self.sagittal, axes = (2, 1))
        self.axial = np.rot90(self.axial, axes = (2, 1), k = 2)
        # преобразовать pixel_array

class DicomVolumeSPECT():
    def __init__(self, pixel_array, meta):
        self.meta = meta
        self.pixel_array = pixel_array

        # pixel aspects, assuming all slices are the same
        self.coronal_aspect = meta.SliceThickness/meta.PixelSpacing[0]
        self.sagittal_aspect = meta.PixelSpacing[1]/meta.SliceThickness #* 16
        self.axial_aspect = meta.PixelSpacing[1]/meta.PixelSpacing[0]

        # create 3D array
        self.img_shape = list(pixel_array[0].shape)
        self.img_shape.append(len(pixel_array))
        self.volume = np.zeros(self.img_shape)

        # fill 3D array with the images from the files
        for i, slice in enumerate(pixel_array):
            self.volume[:, :, i] = slice
        
        self.coronal = []
        self.axial = []
        self.sagittal = []
        for i, slice in enumerate(self.volume):
            self.coronal.append(self.volume[i,:,:])
            self.sagittal.append(self.volume[:,i,:].T)
            if i < self.volume.shape[2]:
                self.axial.append(self.volume[:,:,self.volume.shape[2] - i - 1])

        self.coronal = np.rot90(self.coronal, axes = (2, 1), k = 3)
        self.sagittal = np.rot90(self.sagittal, axes = (2, 1), k = 2)
        self.axial = np.rot90(self.axial, axes = (2, 1), k = 2)
        # преобразовать pixel_array

class aCT():
    def __init__(self):
        self.coronal = []
        self.axial = []
        self.sagittal = []

class aSPECT():
    def __init__(self):
        self.coronal = []
        self.axial = []
        self.sagittal = []