import matplotlib.pyplot as plt
import numpy as np
import cv2
from skimage.transform import resize 
from skimage.transform import rotate
from skimage.transform import AffineTransform, warp
from clipped_zoom import cv2_clipped_zoom
from dicomVolume import DicomVolumeSPECT, DicomVolumeCT, aSLICES
from PIL import Image, ImageTk
WINDOW_CENTER = -400
WINDOW_WIDTH = 1500

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
    a_CT.meta = CT.meta
    a_SPECT.meta = SPECT.meta

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

def window_ct(dcm, w = 1500, c = -400, ymin = 0, ymax = 255, meta = ''):
    """Windows a CT slice.
    http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.11.2.html

    Args:
        dcm (pydicom.dataset.FileDataset):
        w: Window Width parameter.
        c: Window Center parameter.
        ymin: Minimum output value.
        ymax: Maximum output value.

    Returns:
        Windowed slice.
    """
    try:
        # convert to HU
        b = dcm.RescaleIntercept
        m = dcm.RescaleSlope
        x = m * dcm.pixel_array + b
    except:
        b = meta.RescaleIntercept
        m = meta.RescaleSlope
        x = m * dcm + b
    # windowing C.11.2.1.2.1 Default LINEAR Function
    #
    y = np.zeros_like(x)
    y[x <= (c - 0.5 - (w - 1) / 2)] = ymin
    y[x > (c - 0.5 + (w - 1) / 2)] = ymax
    y[(x > (c - 0.5 - (w - 1) / 2)) & (x <= (c - 0.5 + (w - 1) / 2))] = \
        ((x[(x > (c - 0.5 - (w - 1) / 2)) & (x <= (c - 0.5 + (w - 1) / 2))] - (c - 0.5)) / (w - 1) + 0.5) * (
                ymax - ymin) + ymin

    return y

def calclate_accumulation(CT, SPECT, MASKS):
    r_top_masks = np.copy(MASKS)
    r_top_masks[r_top_masks != 1] = 0
    r_mid_masks = np.copy(MASKS)
    r_mid_masks[r_mid_masks != 2] = 0
    r_bot_masks = np.copy(MASKS)
    r_bot_masks[r_bot_masks != 3] = 0
    l_top_masks = np.copy(MASKS)
    l_top_masks[l_top_masks != 4] = 0
    l_bot_masks = np.copy(MASKS)
    l_bot_masks[l_bot_masks != 5] = 0

    r_top = np.sum(r_top_masks * SPECT.coronal)
    r_mid = np.sum(r_mid_masks * SPECT.coronal)
    r_bot = np.sum(r_bot_masks * SPECT.coronal)
    l_top = np.sum(l_top_masks * SPECT.coronal)
    l_bot = np.sum(l_bot_masks * SPECT.coronal)

    return r_top, r_mid, r_bot, l_top, l_bot

def overlay(ct, mask, spect, do_mask = False):
    if do_mask:
        colormap = plt.get_cmap('magma')
        heatmap = (colormap(mask*48) * 2**16).astype(np.uint16)[:,:,:3]

        colormap2 = plt.get_cmap('gray')
        heatmap2 = (colormap2(ct/512) * 2**16).astype(np.uint16)[:,:,:3]
        heatmap2 = cv2.cvtColor(heatmap2, cv2.COLOR_RGB2BGR)

        result = cv2.addWeighted(heatmap, 0.9, heatmap2, 1.2, 0)/256
        result = result.astype(np.uint8)
        img =  ImageTk.PhotoImage(image=Image.fromarray(result).resize((256,256), resample = Image.NEAREST))
        return img

    else:
        colormap = plt.get_cmap('inferno')
        heatmap = (colormap(spect/768) * 2**16).astype(np.uint16)[:,:,:3]

        colormap2 = plt.get_cmap('gray')
        heatmap2 = (colormap2(ct/512) * 2**16).astype(np.uint16)[:,:,:3]
        heatmap2 = cv2.cvtColor(heatmap2, cv2.COLOR_RGB2BGR)

        result = cv2.addWeighted(heatmap, 0.9, heatmap2, 1.2, 0)/256
        result = result.astype(np.uint8)
        img =  ImageTk.PhotoImage(image=Image.fromarray(result).resize((256,256), resample = Image.NEAREST))

        return img


def make_image(cur_study, isresult = False):
    if not isresult:
        try: #первый ключ - серия, второй - номер снимка (средний снимок)
            try:
                array = window_ct(cur_study[len(cur_study)//2], WINDOW_WIDTH, WINDOW_CENTER, 0, 255) # Если это серия КТ
            except:
                array = cur_study[len(cur_study)//2].pixel_array # это если серия ОФЭКТ
        except:
            if len(cur_study.pixel_array.shape) == 3:
                array = cur_study.pixel_array[len(cur_study.pixel_array)//2] # это если файл ОФЭКТ
            else:
                array = cur_study.pixel_array # если это файл КТ
    else:
        array = cur_study
        
    img =  ImageTk.PhotoImage(image=Image.fromarray(array).resize((256,256), resample = Image.NEAREST))
    return img
