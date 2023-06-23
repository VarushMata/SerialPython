#Mata Prieto Varush
#Reconocer el color más predominante de una imagen (Rojo, Verde o Azul)
#Y mandar a un Arduino la instrucción para encender un led dependiendo 
#del color dominante
import serial,time
import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import numpy as np

class VentanaParaOpenCV:
    def __init__(self,ventana):
        self.arduino = serial.Serial("COM7", 9600, timeout=1.0)
        time.sleep(1)
        self.btn=Button(ventana,text="Seleccionar imagen",command=self.seleccionarImg)
        self.btn.grid(column=0,row=0)
        self.lblI=Label(ventana,text="IMAGEN",font="bold").grid(column=1,row=0)
        self.lblImage=Label(ventana)
        self.lblImage.grid(column=1,row=1,rowspan=14)
        self.rb0=Button(ventana,text='Identificar color dominante',command=self.color_prim)
        self.rb0.grid(column=0, row=3, sticky=W)
        

    def seleccionarImg(self):
        path_image=filedialog.askopenfilename(filetypes=[("image",".jpeg",),("image",".png"),("image",".jpg")])
        if len(path_image) > 0:
            self.image=cv2.imread(path_image)
            imageToShow=cv2.cvtColor(self.image,cv2.COLOR_BGR2RGB)
            im=Image.fromarray(imageToShow)
            img=ImageTk.PhotoImage(image=im)
            self.lblImage.configure(image=img)
            self.lblImage.image=img


    def create_bar(self,height,width,color):
        bar = np.zeros((height,width,3),np.uint8)
        bar[:] = color
        red, green, blue = int(color[2]), int(color[1]), int(color[0])
        return bar, (red, green, blue)


    def color_prim(self):
        height, width, _ = np.shape(self.image)

        data = np.reshape(self.image, (height * width , 3))
        data = np.float32(data)

        clusters = 1
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        flags = cv2.KMEANS_RANDOM_CENTERS
        _ , _ , centers = cv2.kmeans(data, clusters, None, criteria, 10, flags)

        bars = []
        rgb_values = []

        for index, row in enumerate(centers):
            bar, rgb = self.create_bar(200, 200, row)
            bars.append(bar)
            rgb_values.append(rgb)
      
        for index, row in enumerate(rgb_values):
            print(f'{index + 1}.RGB{row}')
        
        if rgb_values[0][0] > rgb_values[0][1]:
            if rgb_values[0][0] > rgb_values[0][2]:
                self.arduino.write(b'R')
                print('led1')

        elif rgb_values[0][1] > rgb_values[0][2]:
            self.arduino.write(b'G')
            print('led2')

        else:
            self.arduino.write(b'B')
            print('led3')
        
ventana = Tk()
VentanaParaOpenCV(ventana)   
ventana.mainloop()


 




