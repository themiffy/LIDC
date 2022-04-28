import matplotlib.pyplot as plt

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

import predict

if __name__ == "__main__":

    ######################################## Buttons commands #####################################

    def btn1_com():
        global file
        file = filedialog.askopenfilename(filetypes = (("Jpeg images","*.jpg"),("all files","*.*")))

        pred, image = predict.make_prediction(file)

        alpha = 0.2 # amount of transparency
        f, axarr = plt.subplots(1,3)
        axarr[0].imshow(pred)
        axarr[1].imshow(image)
        axarr[2].imshow(pred * alpha + image * (1-alpha))
        plt.show()


    ###############################################################################################


    window = Tk()
    window.title('Программа')
    window.geometry('500x500')
    btn1 = Button(window, text="Загрузить изображение", command = btn1_com, padx=5, pady=5)
    btn1.grid(column = 0, row = 0)


    window.mainloop()
