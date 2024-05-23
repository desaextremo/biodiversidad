'''
funciones_captura.py: Define funciones de utilidad para la captura datos enteros, flotante,
limpiado de pantalla, tiempo de espera y menu de opciones.

Para utilizar las funciones definidas en este programa solo se requiere incluir al inicio de su programa
la instrucción:

#Referencia a todos las funciones en el archivo .py
from funciones_captura import * 
'''

import os
import time

def tiempo_espera(time_duration):
    '''Esta función define un tiempo de espera antes de realizar una proxima accción'''
    time.sleep(time_duration)

def pausa():
    '''Esta función ejecuta el comando pause, solo es valida en windows'''
    os.system("pause")
    
def limpiar_pantalla():
    '''
    Esta función se encarga de validar el sistema operativo anfitrion y ejecutar el comando de limpiar pantalla
    '''
    print(os.name)

    
    if os.name=="Linux" or os.name=="posix":
        os.system("clear")
    else:
        os.system("cls")

def leer_cadena(mensaje, mensaje_error):
    """
    Solicita al usuario ingresar una cadena de caracteres.
    
    Parámetros:
        mensaje (str): Mensaje a mostrar al usuario para solicitar la cadena.
        mensaje_error (str): Mensaje a mostrar en caso de que se produzca un error.
    
    Retorna:
        str: La cadena de caracteres ingresada por el usuario.
    """
    while True:
        try:
            cadena = input(mensaje)
            # Verificar si la cadena no está vacía después de eliminar los espacios en blanco
            if cadena.strip():
                return cadena
            else:
                raise ValueError  # Lanzar una excepción si la cadena es vacía
        except ValueError:
            print(mensaje_error)          

#def <nombre de la funcion> (<parametros separados por ,>) return <valor>
def leer_entero(mensaje, mensaje_error):
    '''
    Esta función captura un valor e intenta convertirlo a entero, control la
    exepción si la conversión falla, y solicita el valor tantas veces como sea
    necesario, hasta que este sea un número entero

    params: 
    return: valor entero
    '''
    valor=0
    estado=False
    while(estado==False):
        try:
            valor=int(input(mensaje))
            estado=True
        except ValueError as error:
            print(mensaje_error)

    return valor

def leer_flotante(mensaje, mensaje_error):
    '''
    Esta función captura un valor e intenta convertirlo a flotante, control la
    exepción si la conversión falla, y solicita el valor tantas veces como sea
    necesario, hasta que este sea un número flotante

    params: 
    return: valor flotante
    '''
    valor=0
    estado=False
    while(estado==False):
        try:
            valor=float(input(mensaje))
            estado=True
        except ValueError as error:
            print(mensaje_error)

    return valor

def presenta_menu(menu,valorMinimo,valorMaximo):
    '''
    Esta función se encarga de presentar un menu de opciones al usuario y validar
    que su eleccion este dentro del rango de valores permitidos.

    params: menu Listado de opciones
            valorMinimo opcion de menor valor
            valorMaximo opcion de mayor valor
    return: valor la opcion seleccionada por el usuario
    '''
    opcion=0
    while(opcion==0):
        opcion=leer_entero(menu,f"Debe ingresar una opción numérica entre {valorMinimo} y {valorMaximo}")

        if opcion < valorMinimo or opcion > valorMaximo:
            print(f"Debe ingresar una opción entre {valorMinimo} y {valorMaximo}")
            opcion=0
            
    return opcion