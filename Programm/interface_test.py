from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from skimage.io import imread, imshow # input and output
import matplotlib.pyplot as plt

def btn1_com():
    global file
    file = filedialog.askopenfilename(filetypes = (("Jpeg images","*.jpg"),("all files","*.*")))
    image = imread(file)
    imshow(image)
    plt.show()

window = Tk()
window.title('Программа')
window.geometry('500x500')
btn1 = Button(window, text="Загрузить изображение", command = btn1_com, padx=5, pady=5)
btn1.grid(column = 0, row = 0)


window.mainloop()