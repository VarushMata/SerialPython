from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import cv2
import numpy as np
import matplotlib.pyplot as plt

class VentanaParaOpenCV:
    def __init__(self,ventana):
        self.btn=Button(ventana,text="Seleccionar imagen",command=self.seleccionarImg)
        self.btn.grid(column=0,row=0)
        self.lbl=Label(ventana,text="IMAGEN",font="bold").grid(column=1,row=0)
        self.lblImage=Label(ventana)
        self.lblImage.grid(column=1,row=1,rowspan=14)
        self.lblI=Label(ventana,text="Seleccione el filtro que desea aplicar: ")
        self.lblI.grid(column=0,row=2)
        self.grupoFiltro=IntVar()
        self.rb0=Radiobutton(ventana,text='Original',value=0,variable=self.grupoFiltro,command=self.filtrar)
        self.rb1=Radiobutton(ventana,text='Escala de grises',value=1,variable=self.grupoFiltro,command=self.filtrar)
        self.rb2=Radiobutton(ventana,text='Rotar 90º',value=2,variable=self.grupoFiltro,command=self.filtrar)
        self.rb3=Radiobutton(ventana, text='Difuminar', value=3,variable=self. grupoFiltro, command= self.filtrar)
        self.rb4=Radiobutton(ventana, text='Obtener bordes', value=4,variable=self. grupoFiltro, command= self.filtrar)
        self.rb5=Radiobutton(ventana, text='Componente azul (RGB)',value=5, variable=self. grupoFiltro, command= self.filtrar)
        self.rb6=Radiobutton(ventana, text='Filtro amarillo (HSV)',value=6, variable=self. grupoFiltro, command= self.filtrar)
        self.rb7=Radiobutton(ventana, text='Resaltar amarillo', value=7,variable=self. grupoFiltro, command= self.filtrar)
        self.rb8=Radiobutton(ventana, text='Resaltar rojo', value=8,variable=self. grupoFiltro, command= self.filtrar)
        self.rb9=Radiobutton(ventana, text='Resaltar azul', value=9,variable=self. grupoFiltro, command= self.filtrar)
        self.rb0.grid(column=0, row=3, sticky=W)
        self.rb1.grid(column=0, row=4, sticky=W)
        self.rb2.grid(column=0, row=5, sticky=W)
        self.rb3.grid(column=0, row=6, sticky=W)
        self.rb4.grid(column=0, row=7, sticky=W)
        self.rb5.grid(column=0, row=8, sticky=W)
        self.rb6.grid(column=0, row=9, sticky=W)
        self.rb7.grid(column=0, row=10, sticky=W)
        self.rb8.grid(column=0,row=11,sticky=W)
        self.rb9.grid(column=0,row=12,sticky=W)
        
    def seleccionarImg(self):
        path_image=filedialog.askopenfilename(filetypes=[("image",".jpeg",),("image",".png"),("image",".jpg")])
        if len(path_image)>0:
            self.image=cv2.imread(path_image)
            imageToShow=cv2.cvtColor(self.image,cv2.COLOR_BGR2RGB)
            im=Image.fromarray(imageToShow)
            img=ImageTk.PhotoImage(image=im)
            self.lblImage.configure(image=img)
            self.lblImage.image=img

    def filtrar(self):
        
        if self.grupoFiltro.get()==0:
            imagenDeSalida=cv2.cvtColor(self.image,cv2.COLOR_BGR2RGB)

        elif self.grupoFiltro.get()==1:
            imagenDeSalida=cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)

        elif self.grupoFiltro.get()==2:
            alto,ancho=self.image.shape[:2]
            centro=(alto/2,ancho/2)
            rotate_matriz=cv2.getRotationMatrix2D(center=centro,angle=90,scale=1)
            imagenrotada=cv2.warpAffine(src=self.image,M=rotate_matriz,dsize=(alto,ancho))
            imagenDeSalida=cv2.cvtColor(imagenrotada,cv2.COLOR_BGR2RGB)

        elif self.grupoFiltro.get()==3:
            difuminada=cv2.medianBlur(self.image,9)
            imagenDeSalida=cv2.cvtColor(difuminada,cv2.COLOR_BGR2RGB)

        elif self.grupoFiltro.get()==4:
            bordes=cv2.Canny(self.image,50,100)
            imagenDeSalida=cv2.cvtColor(bordes,cv2.COLOR_BGR2RGB)

        elif self.grupoFiltro.get()==5:
            imagen_azul=self.image.copy()
            imagen_azul [:,:,0]=0
            imagen_azul [:,:,1]=0
            imagenDeSalida=cv2.cvtColor(imagen_azul,cv2.COLOR_BGR2RGB)
            plt.imshow(imagen_azul)

        elif self.grupoFiltro.get()==6:
            imagen_rgb=cv2.cvtColor(self.image,cv2.COLOR_BGR2RGBA)
            imagen_hsv=cv2.cvtColor(imagen_rgb,cv2.COLOR_RGB2HSV)
            #rangos de amarillo
            rojoBajo=np.array([22,100,200],np.uint8)
            rojoAlto=np.array([38,255,255],np.uint8)
            #creación máscara   
            mascara_amarilla=cv2.inRange(imagen_hsv,rojoBajo,rojoAlto)
            segmentada_amarilla=cv2.bitwise_and(imagen_rgb,imagen_rgb,mask=mascara_amarilla)
            #regresando a BGR
            amarillo=cv2.cvtColor(segmentada_amarilla,cv2.COLOR_RGB2BGR)
            imagenDeSalida=cv2.cvtColor(amarillo,cv2.COLOR_BGR2RGB)

        elif self.grupoFiltro.get()==7:
            imagen_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGBA)
            amarilloBajo = np.array([22,100,200], np.uint8)
            amarilloAlto = np.array([38, 255, 255], np.uint8)
            imagen_hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
            mascaraAmarilla = cv2.inRange(imagen_hsv, amarilloBajo,amarilloAlto)
            colorAmarillo = cv2.bitwise_and(self.image, self.image,mask=mascaraAmarilla)
            gris = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            gris = cv2.cvtColor(gris, cv2.COLOR_GRAY2BGR)
            invMask = cv2.bitwise_not(mascaraAmarilla)
            bgGray = cv2.bitwise_and(gris, gris, mask=invMask)
            finalImage = cv2.add(bgGray, colorAmarillo)
            imagenDeSalida = cv2.cvtColor(finalImage, cv2.COLOR_BGR2RGB)

        elif self.grupoFiltro.get()==8:
            imagen_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGBA)
            rojoBajo = np.array([0,100,20], np.uint8)
            rojoAlto = np.array([10,255,255], np.uint8)
            imagen_hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
            mascaraRoja = cv2.inRange(imagen_hsv, rojoBajo,rojoAlto)
            colorRojo = cv2.bitwise_and(self.image, self.image,mask=mascaraRoja)
            gris = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            gris = cv2.cvtColor(gris, cv2.COLOR_GRAY2BGR)
            invMask = cv2.bitwise_not(mascaraRoja)
            bgGray = cv2.bitwise_and(gris, gris, mask=invMask)
            finalImage = cv2.add(bgGray, colorRojo)
            imagenDeSalida = cv2.cvtColor(finalImage, cv2.COLOR_BGR2RGB)

        elif self.grupoFiltro.get()==9:
            imagen_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGBA)
            azulBajo = np.array([100,100,20], np.uint8)
            azulAlto = np.array([125,255,255], np.uint8)
            imagen_hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
            mascaraAzul = cv2.inRange(imagen_hsv, azulBajo,azulAlto)
            colorAzul = cv2.bitwise_and(self.image, self.image,mask=mascaraAzul)
            gris = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            gris = cv2.cvtColor(gris, cv2.COLOR_GRAY2BGR)
            invMask = cv2.bitwise_not(mascaraAzul)
            bgGray = cv2.bitwise_and(gris, gris, mask=invMask)
            finalImage = cv2.add(bgGray, colorAzul)
            imagenDeSalida = cv2.cvtColor(finalImage, cv2.COLOR_BGR2RGB)

        im=Image.fromarray(imagenDeSalida)
        img=ImageTk.PhotoImage(image=im)
        self.lblImage.configure(image=img)
        self.lblImage.image=img
ventana = Tk()
VentanaParaOpenCV(ventana)     
ventana.mainloop()