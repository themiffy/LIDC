import pydicom 
import matplotlib.pyplot as plt
from skimage.io import imread, imshow 
import glob
import numpy as np

print('\n-----------------------------------------')
filenames = glob.glob('LUNG_SPECT_CT/DICOM/17102719/25530000/*')
i = 0
ar_dicoms = []

for file in filenames: 
    ar_dicoms.append(pydicom.dcmread(file))
    i += 1

print(f"Filenames: {i}, Dataset consists of: {len(ar_dicoms)}")

for i, element in enumerate(ar_dicoms):
    if element.SOPClassUID == '1.2.840.10008.5.1.4.1.1.20':
        print(i)
        print(element.pixel_array.shape)
    
#print(ar_dicoms[7].pixel_array.shape)
#print(ar_dicoms[7].SOPClassUID)
#imshow(ar_dicoms[134].pixel_array)
#print(ar_dicoms[182].pixel_array.shape)
#plt.show()

print(ar_dicoms[197])
print('\n-----------------------------------------')


print(pydicom.dcmread('I0.dcm'))