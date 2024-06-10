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
@app.get("/consultar/{tipo_consulta}/{inferior}/{superior}")
def retornar_datos(tipo_consulta: int,inferior: int,superior: int):
    datos = []
    nombre_archivo = 'animales_boyaca.json'

    if tipo_consulta==1:
        nombre_archivo = "animales_boyaca.json"
    elif tipo_consulta==2:
        nombre_archivo = "animales_cundinamarca.json"
    elif tipo_consulta==3:
        nombre_archivo = "hongos_boyaca.json"
    elif tipo_consulta==4:
        nombre_archivo = "hongos_cundinamarca.json"
    elif tipo_consulta==5:
        nombre_archivo = "plantas_boyaca.json"
    elif tipo_consulta==6:
        nombre_archivo = "plantas_cundinamarca.json"
        #abrir el contenido del archivo en una lista

    with open(nombre_archivo,"r",encoding="utf8") as archivo:
        datos = json.load(archivo)

        longitud =len(datos)
        
        datos = datos[inferior-1:superior]

        datos.insert(0,{"rows":longitud})
    
    return datos

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)