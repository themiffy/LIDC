import matplotlib.pyplot as plt
from skimage.transform import resize 
from skimage.transform import rotate
from skimage.transform import AffineTransform, warp
from clipped_zoom import cv2_clipped_zoom
from dicomVolume import DicomVolumeSPECT, DicomVolumeCT, aSLICES

def analyze(CT, SPECT, MASK = ''):
    sl = 126*4
    print('CT: ', len(CT.pixel_array), CT.pixel_array[0].shape)
    print('SPECT: ', len(SPECT.pixel_array), SPECT.pixel_array[0].shape)
   

    #pos = CT.meta.ImagePosition + x * CT.meta.PixelSpacing[0] * CT.meta.ImageOrientation[0...2] + y * CT.meta.PixelSpacing[1] * CT.meta.ImageOrientation[3...5]

    # сделать подписи - что на какой плоскости
    
    a2 = plt.subplot(2, 2, 1)
    plt.imshow(CT.coronal[sl])
    a2.set_aspect(CT.coronal_aspect)

    a1 = plt.subplot(2, 2, 2)
    plt.imshow(CT.sagittal[sl])
    a1.set_aspect(CT.sagittal_aspect)

    a3 = plt.subplot(2, 2, 3)
    plt.imshow(CT.axial[sl//4])
    a3.set_aspect(CT.axial_aspect)
    
    plt.show()

#----------------------------------------
    spect_slice = int((128 - 128/(SPECT.meta.ReconstructionDiameter/CT.meta.ReconstructionDiameter)) 
                        / 2 + sl/(SPECT.meta.ReconstructionDiameter/CT.meta.ReconstructionDiameter*4))


    a2 = plt.subplot(2, 2, 1)
    plt.imshow(SPECT.coronal[spect_slice])
    a2.set_aspect(SPECT.coronal_aspect)

    a1 = plt.subplot(2, 2, 2)
    plt.imshow(SPECT.sagittal[spect_slice])
    a1.set_aspect(SPECT.sagittal_aspect)

    a3 = plt.subplot(2, 2, 3)
    plt.imshow(SPECT.axial[spect_slice])
    a3.set_aspect(SPECT.axial_aspect)


    plt.show()

    img = resize(CT.coronal[sl], (256, 256), mode='constant', preserve_range=True)
    img2 = resize(SPECT.coronal[spect_slice], (256, 256), mode='constant', preserve_range=True)
    #img2 = rotate(img2, 180)
    img2 = cv2_clipped_zoom(img2, SPECT.meta.ReconstructionDiameter/CT.meta.ReconstructionDiameter)
    affine = AffineTransform(translation = (5, 40))
    img2 = warp(img2, affine.params, mode = 'constant')
    alpha = 0.1 # amount of transparency
    smth = img * alpha + img2 * (1 - alpha)

    plt.imshow(smth)
    plt.show()
    return spect_slice

def align(CT, SPECT):
    
    a_CT = aSLICES()
    a_SPECT = aSLICES()
    affine = AffineTransform(translation = (5, 40))

    for i in range(len(SPECT.coronal) - 1): # -1??
        i *= 4
        spect_slice_num = int((128 - 128/(SPECT.meta.ReconstructionDiameter/CT.meta.ReconstructionDiameter)) 
                        / 2 + i/(SPECT.meta.ReconstructionDiameter/CT.meta.ReconstructionDiameter*4))

        ct_coronal = resize(CT.coronal[i], (256, 256), mode='constant', preserve_range=True)
        spect_coronal = resize(SPECT.coronal[spect_slice_num], (256, 256), mode='constant', preserve_range=True)
        spect_coronal = cv2_clipped_zoom(spect_coronal, SPECT.meta.ReconstructionDiameter/CT.meta.ReconstructionDiameter)
        spect_coronal = warp(spect_coronal, affine.params, mode = 'constant')
        
        ct_sagittal = resize(CT.sagittal[i], (256, 256), mode='constant', preserve_range=True)
        spect_sagittal = resize(SPECT.sagittal[spect_slice_num], (256, 256), mode='constant', preserve_range=True)
        spect_sagittal = cv2_clipped_zoom(spect_sagittal, SPECT.meta.ReconstructionDiameter/CT.meta.ReconstructionDiameter)
        spect_sagittal = warp(spect_sagittal, affine.params, mode = 'constant')

        ct_axial = resize(CT.axial[i//4], (256, 256), mode='constant', preserve_range=True)
        spect_axial = resize(SPECT.axial[spect_slice_num], (256, 256), mode='constant', preserve_range=True)
        spect_axial = cv2_clipped_zoom(spect_axial, SPECT.meta.ReconstructionDiameter/CT.meta.ReconstructionDiameter)
        #spect_axial = warp(spect_axial, affine.params, mode = 'constant')
        

        a_CT.coronal.append(ct_coronal)
        a_SPECT.coronal.append(spect_coronal)

        a_CT.sagittal.append(ct_sagittal)
        a_SPECT.sagittal.append(spect_sagittal)

        a_CT.axial.append(ct_axial)
        a_SPECT.axial.append(spect_axial)

    return a_CT, a_SPECT

def structuralize_dataset(ar_dicoms, keys):
    data = {key: [] for key in keys}

    for dcm in ar_dicoms:
        data[dcm.SeriesNumber].append(dcm)

    for key, array in data.items():
        array.sort(key = lambda x: x.InstanceNumber) # сортировка по номеру в серии
    
    return data