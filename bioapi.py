'''
1 Importar FastAPI para exponer consulta
2 Definit métodos de consulta
'''

from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import json

#Llamamos a FastAPI, y desde este momento haremos referencia a este mediante la variable 'app'
app = FastAPI()

# Permitir solicitudes desde todos los orígenes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir esto a los orígenes que desees permitir
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

#metodo de consulta para cada uno de los servicios
@app.get("/hongosboyaca")
def hongos_boyaca():
    hongos_boyaca = []
    nombre_archivo = "hongos_boyaca.json"

     #abrir el contenido del archivo en una lista
    with open(nombre_archivo,"r",encoding="utf8") as archivo:
        hongos_boyaca = json.load(archivo)

    return hongos_boyaca


