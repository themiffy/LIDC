from sqlite3 import DatabaseError
import matplotlib.pyplot as plt
import pydicom as dicom
import glob
import numpy as np

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

from PIL import Image, ImageTk

from predict import make_prediction, segment
from utilities import structuralize_dataset, align, window_ct
from dicomVolume import DicomVolumeSPECT, DicomVolumeCT

global DATA

if __name__ == "__main__":

    ######################################## Event Handlers #####################################

    def refresh_study():
        try:
            chooseCT['values'] = list(serNumbers)
            chooseSPECT['values'] = list(serNumbers)
            
        except:
            print('Choose files first!')

    def refresh_files():

        pass

    def ct_study_selected(*args):
        global img
        global canvas

        cur_study = DATA[int(chooseCT.get())]
        img = make_image(cur_study)

        canvas.create_image(0,0, anchor="nw", image=img)
        study_info.config(text = f'Изображений в серии: {len(cur_study)},\n' +
                                f'Модальность: {cur_study[0].Modality}')

    def spect_study_selected(*args):
        global img
        global canvas
        cur_study = DATA[int(chooseSPECT.get())]
        img = make_image(cur_study)

        canvas.create_image(0,0, anchor="nw", image=img)
        study_info.config(text = f'Изображений в серии: {len(cur_study)},\n' +
                                f'Модальность: {cur_study[0].Modality}')

        chooseSPECTfile['values'] = [i for i in range(len(cur_study))]#DATA[int(chooseSPECT.get())] # выбрали серию - обновляем список файлов

    def spect_file_selected(*args):
        global img
        global canvas
        cur_study = DATA[int(chooseSPECT.get())][int(chooseSPECTfile.get())]

        img = make_image(cur_study)
        canvas.create_image(0,0, anchor="nw", image=img)
        image_count = f'{len(cur_study.pixel_array)}' if len(cur_study.pixel_array.shape) == 3 else '1'
        try:
            study_info.config(text = f'Снимков в файле: {image_count}\n' +
                                    f'Вид: {cur_study.DetectorInformationSequence[0].ViewCodeSequence[0].CodeMeaning}')
        except:
            study_info.config(text = f'Снимков в файле: {image_count}')

    def btn1_com():
        global file
        file = filedialog.askopenfilename(filetypes = (("Jpeg images","*.jpg"),("all files","*.*")))

        pred, image = make_prediction(file)

        alpha = 0.2 # amount of transparency
        f, axarr = plt.subplots(1,3)
        axarr[0].imshow(pred)
        axarr[1].imshow(image)
        axarr[2].imshow(pred * alpha + image * (1-alpha))
        plt.show()

    def button_open_study():
        filenames = glob.glob(filedialog.askdirectory() + '/*') # выбираю папку и записываю имена файлов

        global ar_dicoms
        global DATA
        global serNumbers
        serNumbers = set()
        ar_dicoms = []

        for file in filenames: # Читаю dicom
            try:
                ar_dicoms.append(dicom.dcmread(file))
                serNumbers.add(ar_dicoms[-1].SeriesNumber)
            except:
                print('\nFile', file.split('/')[-1], 'is not DICOM!\n')

        DATA = structuralize_dataset(ar_dicoms, serNumbers)

        # Вывожу инфу в интерфейс
        chooseCT['state'] = 'readonly'
        chooseSPECT['state'] = 'readonly'
        chooseSPECTfile['state'] = 'readonly'

        filecount.config(text = f'Количество файлов {len(ar_dicoms)}\n' + 
                                f'Количество серий {len(serNumbers)}:\n') # Информация о файлах
    
    def button_analyze(): # начинается жесть
        global DATA
        results_window = Toplevel(master)
        results_window.title("Результаты")
        results_window.geometry('700x700')
        # подгодовка КТ
        ct_study = DATA[int(chooseCT.get())]
        slices = []
        for el in ct_study:
            slices.append(el.pixel_array)
        CT = DicomVolumeCT(slices, ct_study[0]) # 1-Изображения 2-мета

        # подготовка ОФЭКТ
        spect_file = DATA[int(chooseSPECT.get())][int(chooseSPECTfile.get())]
        try:
            SPECT = DicomVolumeSPECT(spect_file.pixel_array, spect_file)
        except:
            print('Некорректное ОФЭКТ исследование')

        # совмещение
        a_CT, a_SPECT = align(CT, SPECT) # это объекты кт и офэкт подогнанные друг под друга 256х256

        mask = segment(a_CT, orient = 'coronal', window_center = -400, window_width = 1500)

        plt.imshow(mask[50])
        plt.show()


    ###############################################################################################
    ##################################### Просто функции ##########################################

    def make_image(cur_study):
        try: #первый ключ - серия, второй - номер снимка (средний снимок)
            try:
                array = window_ct(cur_study[len(cur_study)//2], 1500, -400, 0, 255) # Если это серия КТ
            except:
                array = cur_study[len(cur_study)//2].pixel_array # это если серия ОФЭКТ
        except:
            if len(cur_study.pixel_array.shape) == 3:
                array = cur_study.pixel_array[len(cur_study.pixel_array)//2] # это если файл ОФЭКТ
            else:
                array = cur_study.pixel_array # если это файл КТ
        
        img =  ImageTk.PhotoImage(image=Image.fromarray(array).resize((256,256), resample = Image.NEAREST))
        return img

    ###############################################################################################

    master = Tk()
    master.title('Программа')
    master.geometry('500x500')
    
    btn1 = Button(master, text="Загрузить изображение", command = btn1_com, padx=5, pady=5)
    #btn1.grid(column = 0, row = 0)
    btn1.place(x = 350, y = 470)

    btn2 = Button(master, text="   Открыть папку с DICOM    ", command = button_open_study, padx=5, pady=5)
    #btn2.grid(column = 0, row = 1)
    btn2.place(x = 6, y = 6)

    filecount = Label(master)
    filecount.place(x = 20, y = 35)

    ctlabel = Label(master, text = 'Серия КТ:')
    ctlabel.place(x = 20, y = 80)

    chooseCT = ttk.Combobox(master, values = [], state="disabled", postcommand=refresh_study)
    chooseCT.bind("<<ComboboxSelected>>", ct_study_selected)
    chooseCT.place(x = 5, y = 105)

    spectlabel1 = Label(master, text = 'Серия ОФЭКТ:')
    spectlabel1.place(x = 20, y = 135)

    chooseSPECT = ttk.Combobox(master, values = [], state="disabled", postcommand = refresh_files)
    chooseSPECT.bind("<<ComboboxSelected>>", spect_study_selected)
    chooseSPECT.place(x = 5, y = 160) # тут хранится ключ исследования ОФЭКТ (при обращении конвертировать в int)

    spectlabel2 = Label(master, text = 'Файл ОФЭКТ:')
    spectlabel2.place(x = 20, y = 195)

    chooseSPECTfile = ttk.Combobox(master, values = [], state="disabled")
    chooseSPECTfile.bind("<<ComboboxSelected>>", spect_file_selected)
    chooseSPECTfile.place(x = 5, y = 220) # тут хранится индекс! файла в текущем исследовании (при обращении  конвертировать в int)
    
    canvas = Canvas(master, width = 256, height = 256)
    canvas.place(x = 235, y = 5)

    study_info = Label(master)
    study_info.place(x = 265, y = 265)

    btn3 = Button(master, text="Расчёт", command = button_analyze, padx=5, pady=5)
    btn3.place(x = 300, y = 450)

    
    master.mainloop()
