import PIL
from PIL import *
import PIL.Image
from tkinter import *

window = Tk()
window.title("Esteganografia")
window.geometry("1000x1000")
panel = Frame()
panel.pack()
panel.config(width="1000", heigh="1000")

#label de titulo
titulo=Label(text="Esteganografia")
titulo.pack()
titulo.place(x=10,y=10)

#entrada de datos
#entrada de texto a ocultar
textOcult=Label(text="Ingrese el texto a ocultar :")
textOcult.pack()
textOcult.place(x=50,y=40)
txtTextOcult=Entry()
txtTextOcult.pack()
txtTextOcult.place(x=375,y=40)

#entrada de clabe pibrada
clabePublica=Label(text="Ingrese clabe :")
clabePublica.pack()
clabePublica.place(x=50,y=80)
txtClabePublica=Entry()
txtClabePublica.pack()
txtClabePublica.place(x=375,y=80)

#carga de imagen
imagen=Label(text="Ingrese nombre de la imagen con su extencion :")
imagen.pack()
imagen.place(x=50,y=120)
txtImagen=Entry()
txtImagen.pack()
txtImagen.place(x=375,y=120)

#decode o encode
code=Label(text="Ingrese 1 si desea cifrar, ingrese 2 si desea descifrar :")
code.pack()
code.place(x=50,y=160)
txtCode=Entry()
txtCode.pack()
txtCode.place(x=375,y=160)

#decode o encode
nwImg=Label(text="Ingrese el nombre de la nueva imagen con extencion .png :")
nwImg.pack()
nwImg.place(x=50,y=200)
txtNNwImg=Entry()
txtNNwImg.pack()
txtNNwImg.place(x=375,y=200)

#laberesultado
resultado = Label(text="")
resultado.pack()
resultado.place(x=50,y=300)

#label imagen
imagenlab = Label()
imagenlab.pack()
imagenlab.place(x=0,y=350)


# convertir dato a binario
def genData(data):
    #lista de binario
    newd = []
 
    for i in data:
        newd.append(format(ord(i), '08b'))

    return newd


# edita los bits
def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)
 
    for i in range(lendata):
        pix = [value for value in imdata.__next__()[:3] +
                                imdata.__next__()[:3] +
                                imdata.__next__()[:3]]

        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j]% 2 != 0):
                pix[j] -= 1
 
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if(pix[j] != 0):
                    pix[j] -= 1

                else:
                    pix[j] += 1
 
        #8bo pix = 0 seguir leyendo, = 1 final
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if(pix[-1] != 0):
                    pix[-1] -= 1

                else:
                    pix[-1] += 1
 
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1
 
        pix = tuple(pix)

        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]
 

#pixeles modificados en nueva imagen
def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)
 
    for pixel in modPix(newimg.getdata(), data):
        newimg.putpixel((x, y), pixel)

        if (x == w - 1):
            x = 0
            y += 1

        else:
            x += 1
 

#oculta mensage
def encode():
    img = txtImagen.get()
    image = PIL.Image.open(img,'r')
    data = txtTextOcult.get()

    if (len(data) == 0):
        raise ValueError('Data is empty')
 
    newimg = image.copy()
    encode_enc(newimg, data)
    new_img_name = txtNNwImg.get()
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))


# enocntrar texto 
def decode():
    img = txtImagen.get()
    image = PIL.Image.open(img,'r')
 
    data = ''
    imgdata = iter(image.getdata())
 
    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                                imgdata.__next__()[:3] +
                                imgdata.__next__()[:3]]
 
        # string del binario
        binstr = ''
 
        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'

            else:
                binstr += '1'
 
        data += chr(int(binstr, 2))

        if (pixels[-1] % 2 != 0):
            return data





# la funcion del boton
def main():
    clave = txtClabePublica.get()
    a = int(txtCode.get())
    
    if(clave == 'hskjcnd'):
        if (a == 1):
            #llama a la funcion encode
            encode()

        elif (a == 2):
            #obtiene imagen y datos y miestra imagen codificada y el texto
            ima = txtImagen.get()
            imagen = PhotoImage(file = ima)
            imagenlab.config(image = imagen)
            imagenlab.image = imagen
            tectoFinal = decode()
            texto = 'El valor oculto es: ' + tectoFinal
            resultado.config(text=texto)

        else:
            raise Exception("no seleccionaste correctamente si ocultar o encontrar")

    else:
        print('la clabe el incorrecta')
    

#boton que realiza la accion
opcion1 = Button(command=main, text="Realizar operacion")
opcion1.pack()
opcion1.place(x=375, y=240)

window.mainloop()