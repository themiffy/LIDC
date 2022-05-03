import matplotlib.pyplot as plt
import pydicom as dicom
import glob
import numpy as np

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

from PIL import Image, ImageTk

from predict import make_prediction
from utilities import structuralize_dataset


if __name__ == "__main__":

    def refreshValues():
        try:
            chooseCT['values'] = serNumbers
            
        except:
            print('Choose files first!')

    def study_selected(*args):
        global img
        global canvas

        # TODO : достать картинку из серии
        chooseCT.get() # по этому ключу. Это номер серии!

        array = ar_dicoms[50].pixel_array #temporary

        
        img =  ImageTk.PhotoImage(image=Image.fromarray(array).resize((256,256), resample = Image.NEAREST))
        canvas.create_image(0,0, anchor="nw", image=img)


    ######################################## Buttons commands #####################################

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

    def openCT():

        filenames = glob.glob(filedialog.askdirectory() + '/*') # выбираю папку и записываю имена файлов
        global ar_dicoms
        ar_dicoms = []

        global serNumbers
        serNumbers = set()
        for file in filenames: 
            try:
                ar_dicoms.append(dicom.dcmread(file))
                serNumbers.add(ar_dicoms[-1].SeriesNumber)
            except:
                print('File', file.split('/')[-1], 'is not DICOM!')

        serNumbers = [i for i in serNumbers]
        chooseCT['state'] = 'readonly'
        print(serNumbers)
        

        filecount.config(text = f'Количество файлов {len(ar_dicoms)}\n' + 
                                f'Количество серий {len(serNumbers)}:\n') # Информация о файлах

        filecount.pack()

        

        
        

    ###############################################################################################


    master = Tk()
    master.title('Программа')
    master.geometry('500x500')
    
    btn1 = Button(master, text="Загрузить изображение", command = btn1_com, padx=5, pady=5)
    #btn1.grid(column = 0, row = 0)
    btn1.pack()

    btn2 = Button(master, text="Открыть папку с DICOM", command = openCT, padx=5, pady=5)
    #btn2.grid(column = 0, row = 1)
    btn2.pack()
    filecount = Label(master)

    chooseCT = ttk.Combobox(master, values = [], state="disabled", postcommand=refreshValues)
    chooseCT.bind("<<ComboboxSelected>>", study_selected)
    chooseCT.pack()

    canvas = Canvas(master, width = 256, height = 256)
    canvas.pack()

    master.mainloop()
