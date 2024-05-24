'''
    Utilizar FastAPI para exponer metodos de consulta a información de biodiversidad

    Leer el (los) archivo(s), cargar el contenido del archivo en una lista, depurarla
    y regresarla
'''

#1  Agregar sentencias import al inicio del código para usar e instanciar a FastAPI y Uvicorn
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

#Llamamos a FastAPI, y desde este momento haremos referencia a este mediante la variable 'app'
app = FastAPI()

#2 Agregar instrucciones para evitar bloqueos de seguridad tipo CORS
# Permitir solicitudes desde todos los orígenes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir esto a los orígenes que desees permitir
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

'''
Consultar el archivo hongos_cundinamarca.json,
leer información requerida por el frontend
devolver una lista con los datos necesarios
'''

@app.get("/hongoscund")
def hongos_cundinamarca():
    hongos_cundinamarca = []
    #abrir el archivo
    nombre_archivo="hongos_cundinamarca.json"

    with open(nombre_archivo,"r",encoding="utf8") as archivo:
        hongos_cundinamarca = json.load(archivo)

    return hongos_cundinamarca

lista = hongos_cundinamarca()

#print(len(lista))
#print(lista)