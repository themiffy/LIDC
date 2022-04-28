import matplotlib.pyplot as plt
from skimage.transform import resize 
from skimage.transform import rotate
from clipped_zoom import cv2_clipped_zoom

def analyze(CT, SPECT, MASK = ''):
    sl = 255
    print('CT: ', len(CT.pixel_array), CT.pixel_array[0].shape)
    print('SPECT: ', len(SPECT.pixel_array), SPECT.pixel_array[0].shape)
    img = resize(CT.coronal[sl], (256, 256), mode='constant', preserve_range=True)
    img2 = resize(SPECT.coronal[sl//4], (256, 256), mode='constant', preserve_range=True)
    img2 = rotate(img2, 180)
    img2 = cv2_clipped_zoom(img2, SPECT.meta.ReconstructionDiameter/CT.meta.ReconstructionDiameter)
    
    alpha = 0.1 # amount of transparency
    smth = img * alpha + img2 * (1 - alpha)


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
    #plt.imshow(smth)
    #plt.show()
    pass