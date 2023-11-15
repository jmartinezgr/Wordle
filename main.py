from random import choice
import tkinter as tk
from tkinter import messagebox
from copy import deepcopy

class Nodo:
    def __init__(self,value: int = 0) -> None:
        self.value = value
        self.previous = None

    def set_previous(self, nodo: 'Nodo') -> None:
        self.previous = nodo

ventana = tk.Tk()
ventana.title('Wordle')
ventana.geometry('400x200')
ventana.resizable(False, False)

diccionario = set() #diccionario global para verificar si la palabra digitada existe.
vic = 0
der = 0 
def db_random(lenPalabra): #funcion para escoger una palabra aleatoria de cierto tamaño
    global diccionario
    diccionario = set() #reiniciar el diccionario global cuando se pida una palabra nueva
    palabras = [] #para escoger una palabra aleatoria
    with open('base.txt','r',encoding="UTF-8") as dic:
        for a in dic:
            if len(a.strip()) == lenPalabra:
                palabras.append(a.strip())
                diccionario.add(a.strip())
    #print(palabras) ver banco de palabras de tamaño lenPalabra en la consola
    return choice(palabras)


def retornar_colores(dict_palabra: str, intento: str) -> list:
    info = deepcopy(dict_palabra)

    colores = ['' for _ in intento]

    for i in range(len(intento)):
        if intento[i] == palabra[i]:
            colores[i] = 'Verde'        
            if info[intento[i]][0] > 0:
                info[intento[i]][0] -= 1
            else:
                if info[intento[i]].previus is not None:
                    indice = info[intento[i]][1].previous.value
                    info[intento[i]][1] = info[intento[i]][1].previous
                    colores[indice] = 'Gris'
        else:
            if info.get(intento[i]):
                if info[intento[i]][0] > 0:
                    info[intento[i]][0] -= 1
                    nuevo_nodo = Nodo()
                    nuevo_nodo.set_previous(info[intento[i]][1])
                    info[intento[i]][1].value = i
                    info[intento[i]][1] = nuevo_nodo
                    colores[i] = 'Amarillo'
                else:   
                    colores[i] = 'Gris'
            else:
                colores[i] = 'Gris'
    
    print(colores)

    return colores

def conteo_caracteres(palabra: str) -> dict:
    info = dict()

    for char in palabra:
        if info.get(char):
            info[char][0] += 1
        else:
            info[char] = [1, Nodo()]

    return info

def jugar():
    global juego,framearriba,texto,boton_enviar, difficulty,advertencia, vic,der
    difficulty = int(difficulty_entry.get())
    if difficulty < 4 or difficulty > 8:
        result_label.config(text="Dificultad no válida. Debe ser entre 4 y 8 letras.")
    else:
        ventana.destroy()
        juego=tk.Tk() #nueva ventana
        juego.title('Wordle')
        juego.geometry('1000x700')
        juego.resizable(False, False)

        juego.columnconfigure(0,weight=1)
        for xd in range(6):
            juego.rowconfigure(xd, weight=1)

        titulo = tk.Frame(juego, relief="solid", borderwidth=1)
        titulo.grid(row=0,column=0, pady=10)
        
        titulo.rowconfigure(0,weight=1)
        titulo.columnconfigure(0,weight=1)
        titulo.columnconfigure(1,weight=1)

        victorias = tk.Label(titulo, text= f"victorias = {vic}")
        victorias.grid(row=0,column=0, padx=10)

        derrotas = tk.Label(titulo, text= f"derrotas = {der}")
        derrotas.grid(row=0,column=1, padx=10)

        framearriba = tk.Frame(juego, relief="solid", borderwidth=1)
        framearriba.grid(row=1,column=0)

        descripcion = tk.Label(juego, text="Ingrese una palabra") 
        descripcion.grid(row=2,column=0)

        texto = tk.Entry(juego, width=20)
        texto.grid(row=3)

        # Botón para enviar la palabra
        boton_enviar = tk.Button(juego, text="Enviar", command=comprobar_palabra)
        boton_enviar.grid(row=4)

        advertencia = tk.Label(juego, text="")
        advertencia.grid(row=5)

        tablero(difficulty)


def tablero(n):
    global labels, palabra, victoria, contadorjuego, dic_info
    labels = [[None for _ in range(n)] for _ in range(6)]
    palabra = db_random(n) #acá funcion random dependiendo de la dificultad (n)
    dic_info = conteo_caracteres(palabra)
    print(palabra)
    victoria = False
    contadorjuego = 0

    for i in range(6):
        for j in range(n):
            labels[i][j] = tk.Label(framearriba, borderwidth=1, width=8, height=4, relief="solid")
            labels[i][j].grid(row=i, column=j)

    texto.delete(0, tk.END)  # Limpiar la entrada al iniciar una nueva partida

    # Centrar la ventana en la pantalla
    juego.update_idletasks()
    width = juego.winfo_width()
    height = juego.winfo_height()
    x = (juego.winfo_screenwidth() // 2) - (width // 2)
    y = (juego.winfo_screenheight() // 2) - (height // 2)
    juego.geometry('{}x{}+{}+{}'.format(width, height, x, y-19))
    

def comprobar_palabra():
    global victoria, contadorjuego,vic, der
    texto_ingresado = texto.get()
    texto_ingresado = texto_ingresado.lower()
    if len(texto_ingresado)!=difficulty:
        advertencia.config(text=f"ingresa una palabra válida con {difficulty} letras")
    elif  texto_ingresado not in diccionario:
        advertencia.config(text=f"La palabra '{texto_ingresado}' no se encuentra en nuestra base de datos")

    else:
        advertencia.config(text='')
        if palabra == texto_ingresado:
            for j in range(len(labels[contadorjuego])):
                labels[contadorjuego][j].config(text=texto_ingresado[j], bg='green')

            victoria = True
            vic += 1 
            reiniciar('ganar')
        else:
            colores = retornar_colores(dic_info,texto_ingresado)
            for j in range(len(texto_ingresado)):
                if colores[j] == 'Verde':
                    labels[contadorjuego][j].config(text=texto_ingresado[j], bg='green')
                elif colores[j] == 'Amarillo':
                    labels[contadorjuego][j].config(text=texto_ingresado[j], bg='yellow')
                else:
                    labels[contadorjuego][j].config(text=texto_ingresado[j], bg='gray')

            contadorjuego += 1

        if contadorjuego < len(labels) and not victoria:
            texto.delete(0, tk.END)  # Limpiar la entrada para la siguiente palabra
        elif contadorjuego==len(labels) and not victoria:
            der += 1
            reiniciar('perder')


def reiniciar(causa): #cuando pierdes o ganas muestra la advertencia y se reinicia el juego
    if causa=='ganar':
        respuesta = messagebox.showinfo("GANASTE", "GANASTE, ¿Quieres iniciar el juego?")
        if respuesta == 'ok':
            juego.destroy()
            terminar() #esta funcion crea ventana para preguntar la dificultad
    else:
        respuesta = messagebox.showinfo("PERDISTE", "PERDISTE, ¿Quieres iniciar el juego?")
        if respuesta == 'ok':
            juego.destroy()
            terminar()
            
def iniciar(): #genera las dificultades
    global difficulty_entry, result_label
    difficulty_label = tk.Label(ventana, text="Seleccione la dificultad (4-8 letras):")
    difficulty_label.pack(pady=5)
    difficulty_entry = tk.Entry(ventana)
    difficulty_entry.pack(pady=5)
    start_button = tk.Button(ventana, text="Iniciar partida", command=jugar)
    start_button.pack(pady=10)
    result_label = tk.Label(ventana, text="")
    result_label.pack(pady=10)

    # Centrar la ventana en la pantalla
    ventana.update_idletasks()
    width = ventana.winfo_width()
    height = ventana.winfo_height()
    x = (ventana.winfo_screenwidth() // 2) - (width // 2)
    y = (ventana.winfo_screenheight() // 2) - (height // 2)
    ventana.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def terminar(): #se usa cuando pierde o gana para reicniar la ventana
    global ventana
    ventana = tk.Tk()
    ventana.title('Wordle')
    ventana.geometry('400x200')
    ventana.resizable(False, False)
    iniciar()



ventana.after(0, lambda: iniciar())

ventana.mainloop()
