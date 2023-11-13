from random import choice
import tkinter as tk
from tkinter import messagebox

ventana = tk.Tk()
ventana.title('Wordle')
ventana.geometry('400x200')
ventana.resizable(False, False)

diccionario = set() #diccionario global para verificar si la palabra digitada existe.

def db_random(lenPalabra): #funcion para escoger una palabra aleatoria de cierto tamaño
    palabras = []
    with open('base.txt','r',encoding="UTF-8") as dic:
        for a in dic:
            if len(a.strip()) == lenPalabra:
                palabras.append(a.strip())
                diccionario.add(a.strip())
    #print(palabras) ver banco de palabras de tamaño lenPalabra en la consola
    return choice(palabras)

def jugar():
    global juego,framearriba,texto,boton_enviar, difficulty,advertencia
    difficulty = int(difficulty_entry.get())
    if difficulty < 4 or difficulty > 8:
        result_label.config(text="Dificultad no válida. Debe ser entre 4 y 8 letras.")
    else:
        ventana.destroy()
        juego=tk.Tk() #nueva ventana
        juego.title('Wordle')
        juego.geometry('1000x700')
        juego.resizable(False, False)

        framearriba = tk.Frame(juego, relief="solid", borderwidth=1)
        framearriba.pack()

        
        texto = tk.Entry(juego, width=20)
        texto.pack()

        # Botón para enviar la palabra
        boton_enviar = tk.Button(juego, text="Enviar", command=comprobar_palabra)
        boton_enviar.pack()

        advertencia = tk.Label(juego, text="")
        advertencia.pack()

        tablero(difficulty)

def tablero(n):
    global labels, palabra, victoria, contadorjuego
    labels = [[None for _ in range(n)] for _ in range(6)]
    print(labels)
    palabra = db_random(n) #acá funcion random dependiendo de la dificultad (n)
    victoria = False
    contadorjuego = 0

    for i in range(6):
        for j in range(n):
            labels[i][j] = tk.Label(framearriba, borderwidth=1, width=8, height=4, relief="solid")
            labels[i][j].grid(row=i, column=j)

    texto.delete(0, tk.END)  # Limpiar la entrada al iniciar una nueva partida


def comprobar_palabra():
    global victoria, contadorjuego
    texto_ingresado = texto.get()

    if texto_ingresado not in diccionario:
        pass
        #MOSTRAR VENTANA QUE HAGA ALGO
    
    if len(texto_ingresado)!=difficulty : #and texto_ingresado not in set difficulty
        advertencia.config(text=f"ingresa una palabra válida con {difficulty} letras")
    else:
        if palabra == texto_ingresado:
            for j in range(len(labels[contadorjuego])):
                labels[contadorjuego][j].config(text=texto_ingresado[j], bg='green')

            victoria = True
            reiniciar('ganar')
        else:
            for j in range(len(texto_ingresado)):
                if texto_ingresado[j] == palabra[j]:
                    labels[contadorjuego][j].config(text=texto_ingresado[j], bg='green')
                elif texto_ingresado[j] in palabra:
                    labels[contadorjuego][j].config(text=texto_ingresado[j], bg='yellow')
                else:
                    labels[contadorjuego][j].config(text=texto_ingresado[j], bg='gray')

            contadorjuego += 1

        if contadorjuego < len(labels) and not victoria:
            texto.delete(0, tk.END)  # Limpiar la entrada para la siguiente palabra
        else:
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
    difficulty_label.pack()
    difficulty_entry = tk.Entry(ventana)
    difficulty_entry.pack()
    start_button = tk.Button(ventana, text="Iniciar partida", command=jugar)
    start_button.pack()
    result_label = tk.Label(ventana, text="")
    result_label.pack()

def terminar(): #se usa cuando pierde o gana para reicniar la ventana
    global ventana
    ventana = tk.Tk()
    ventana.title('Wordle')
    ventana.geometry('400x200')
    ventana.resizable(False, False)
    iniciar()



ventana.after(0, lambda: iniciar())

ventana.mainloop()
