import matplotlib.pyplot as plt
from skimage.transform import resize 
from skimage.transform import rotate
from clipped_zoom import cv2_clipped_zoom

def analyze(CT, SPECT, MASK = ''):
    sl = 90*4
    print('CT: ', len(CT.pixel_array), CT.pixel_array[0].shape)
    print('SPECT: ', len(SPECT.pixel_array), SPECT.pixel_array[0].shape)
   

    #pos = CT.meta.ImagePosition + x * CT.meta.PixelSpacing[0] * CT.meta.ImageOrientation[0...2] + y * CT.meta.PixelSpacing[1] * CT.meta.ImageOrientation[3...5]

    # сделать подписи - что на какой плоскости
    
    a2 = plt.subplot(2, 2, 1)
    plt.imshow(CT.coronal[sl])
    a2.set_aspect(CT.coronal_aspect)

    a1 = plt.subplot(2, 2, 2)
    plt.imshow(CT.axial[sl])
    a1.set_aspect(CT.axial_aspect)

    a3 = plt.subplot(2, 2, 3)
    plt.imshow(CT.sagittal[sl//4])
    a3.set_aspect(CT.sagittal_aspect)
    plt.show()

#----------------------------------------
    spect_slice = int((128 - 128/(SPECT.meta.ReconstructionDiameter/CT.meta.ReconstructionDiameter)) 
                        / 2 + sl/(SPECT.meta.ReconstructionDiameter/CT.meta.ReconstructionDiameter*4))
    a2 = plt.subplot(2, 2, 1)
    plt.imshow(SPECT.coronal[spect_slice])
    a2.set_aspect(SPECT.coronal_aspect)

    a1 = plt.subplot(2, 2, 2)
    plt.imshow(SPECT.axial[spect_slice])
    a1.set_aspect(SPECT.axial_aspect)

    a3 = plt.subplot(2, 2, 3)
    plt.imshow(SPECT.sagittal[spect_slice])
    a3.set_aspect(SPECT.sagittal_aspect)


    plt.show()

    img = resize(CT.sagittal[sl//4], (256, 256), mode='constant', preserve_range=True)
    img2 = resize(SPECT.sagittal[spect_slice], (256, 256), mode='constant', preserve_range=True)
    #img2 = rotate(img2, 180)
    img2 = cv2_clipped_zoom(img2, SPECT.meta.ReconstructionDiameter/CT.meta.ReconstructionDiameter)
    
    alpha = 0.1 # amount of transparency
    smth = img * alpha + img2 * (1 - alpha)

    plt.imshow(smth)
    plt.show()
    return spect_slice