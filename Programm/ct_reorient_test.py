import pydicom as dicom
import os
import matplotlib.pyplot as plt
import sys
import glob
import numpy as np
from dicomVolume import DicomVolumeSPECT, DicomVolumeCT

filenames = glob.glob('LUNG_SPECT_CT/DICOM/17102719/25530000/*') # выбираю папку и записываю имена файлов
i = 0
ar_dicoms = []

for file in filenames: 
    ar_dicoms.append(dicom.dcmread(file))
    i += 1


print(f"Filenames: {i}, Dataset consists of: {len(ar_dicoms)}", '\n')
inst = [[],[],[],[]] # inst[Номер серии][Номер файла в ar_dicoms]
for i, element in enumerate(ar_dicoms): # У всех файлов StudyID совпадает и равен 1
    if element.Modality == 'CT':
        if element.SeriesNumber < 5:
            inst[element.SeriesNumber].append(i)

print(len(inst[1]), len(inst[2]), len(inst[3]), '\n') # series number 1 - 1 изображение, 2 - 63 изображения, 3 - 127 изоб

#plt.imshow(ar_dicoms[inst[3][30]].pixel_array) # Первая серия - рентген Вторая - какая то мыльная томография Третья - норм
#plt.show()

slices = [[],[]] # 0 мета 1 изображения
temp = []
for i in inst[3]:
    temp.append(ar_dicoms[i])

temp.sort(key = lambda x: x.InstanceNumber) # сортировка по номеру в серии

slices[0] = temp[1]
for el in temp:
    slices[1].append(el.pixel_array)



ct = DicomVolumeCT(slices[1], slices[0]) # создал объект CT
'''
a = plt.subplot()
plt.imshow(ct.sagittal[30])
a.set_aspect(ct.sagittal_aspect)
plt.show()
'''
slices2 = dicom.dcmread('LUNG_SPECT_CT/DICOM/17102719/25530000/77306389')

SPECT = DicomVolumeSPECT(slices2.pixel_array, slices2)
'''
b = plt.subplot()
plt.imshow(SPECT.sagittal[30])
b.set_aspect(SPECT.sagittal_aspect)
plt.show()
'''
from analysis import analyze, align
print(analyze(ct, SPECT))
a_CT, a_SPECT = align(ct, SPECT)

b = plt.subplot()
plt.imshow(a_CT.axial[80])
#b.set_aspect(SPECT.sagittal_aspect)
plt.show()

b = plt.subplot()
plt.imshow(a_SPECT.axial[80])
#b.set_aspect(SPECT.sagittal_aspect)
plt.show()

#print(ct.meta) # SPECT Reconstruction Diameter             DS: '613.78558349609'
# CT Reconstruction Diameter             DS: '366.0'

#print(ct.meta, '\n')
#print(SPECT.meta.Rows * SPECT.meta.PixelSpacing[0], '\n') # PixelSpacing
#print(ct.meta.Rows * ct.meta.PixelSpacing[0])

print(SPECT.meta.PixelSpacing[0], '\n')
print(ct.meta.PixelSpacing[0])

#print(SPECT.meta[0x0020, 0x0032]) # ImagePositionPatient
print(SPECT.meta.DetectorInformationSequence[0].ImagePositionPatient)
print(temp[126].ImagePositionPatient)
