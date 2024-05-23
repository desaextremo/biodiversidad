#1 uso de requests para consumir datos de una web o de un ws
import json
import requests
from funciones_captura import limpiar_pantalla

# Nombre del archivo JSON de salida
nombre_archivo = "aves.json"

#2 definir una url para consumir o consultar
url = "https://api.catalogo.biodiversidad.co/record_search/advanced_search?class=Aves&department=CO-BOY&size=300"

#3 usar metodo get del paquete requests
response = requests.get(url)

limpiar_pantalla()

aves = []
lista_id = []

if response.status_code == 200:
    listado = response.json()

    #recorrer la lista obteniendo información 
    for indice,datos in enumerate(listado):
        #guardo el id en el listado para consutlar luego
        lista_id.append(datos.get("_id"))

        #diccionario de cada una de las aves, su llave es el _id y su contenido es el diccionario 'datos_ave'
        ave = {}
        #datos del ave
        datos_ave = {}          
        
        #leo y almaceno en el diccionario 'datos_ave' la información general de cada una de las aves
        datos_ave["exotic"]= datos.get("originAtomized").get("exotic")
        datos_ave["invasive"] = datos.get("originAtomized").get("invasive")
        datos_ave["name_scientific"] = datos.get('taxonRecordNameApprovedInUse').get("taxonRecordName").get("scientificName").get("canonicalName").get("simple")
        datos_ave["name_common"] = datos.get('commonNames')[0].get("name")
        datos_ave["names"] = datos.get('commonNames')
        datos_ave["general_desc"] = datos.get("fullDescriptionApprovedInUse").get("fullDescription").get("fullDescriptionUnstructured")
        datos_ave["img_main"] = datos.get("imageInfo").get("mainImage")
        datos_ave["img_thumbnail"] = datos.get("imageInfo").get("thumbnailImage")

        #agrega a cada id, los datos del ave
        ave[datos.get("_id")] = datos_ave

        #agrero cada una de las aves al lsitado 'aves'
        aves.append(ave)

    #imprime la lista de aves
    #print(aves)
    #print(lista_id)


else:
    print(f"Por favor validar la solicitud {response.status_code}")

'''
Peticion detallada de los datos de cada ave
'''
#Recorrer la lisa de id, obteniendo el respectivo id y realziando la consulta de la url
for  indice, valor in enumerate(lista_id):   
    #Segunda peticion
    url_dos = f"https://api.catalogo.biodiversidad.co/complete-record/{valor}"

    #realizar la peticion
    response = requests.get(url_dos)

    #preguntamos si fue exitosa la peticion
    if response.status_code == 200:
        aves_diccionario = response.json()
        datos_ave = {}
        '''
        print(aves_diccionario.get("feedingApprovedInUse").get("feeding").get("feedingUnstructured"))
        print(aves_diccionario.get("behaviorApprovedInUse").get("behavior").get("behaviorUnstructured"))
        print(aves_diccionario.get("habitatsApprovedInUse").get("habitats").get("habitatUnstructured"))
        print(aves_diccionario.get("hierarchy")[0].get("kingdom"))
        print(aves_diccionario.get("hierarchy")[0].get("phylum"))
        print(aves_diccionario.get("hierarchy")[0].get("classHierarchy"))
        print(aves_diccionario.get("hierarchy")[0].get("order"))
        print(aves_diccionario.get("hierarchy")[0].get("family"))
        print(aves_diccionario.get("hierarchy")[0].get("genus"))
        '''

        #obtengo el diccionario con el id y contenido del ave
        ave = aves[indice]

        #obtengo los datos del ave a partir de su id
        datos_ave = ave.get(valor)
        
        datos_ave["feeding"] = aves_diccionario.get("feedingApprovedInUse").get("feeding").get("feedingUnstructured")
        datos_ave["behavior"] = aves_diccionario.get("behaviorApprovedInUse").get("behavior").get("behaviorUnstructured")
        datos_ave["habitats"] = aves_diccionario.get("habitatsApprovedInUse").get("habitats").get("habitatUnstructured")
        datos_ave["kingdom"] = aves_diccionario.get("hierarchy")[0].get("kingdom")
        datos_ave["phylum"] = aves_diccionario.get("hierarchy")[0].get("phylum")
        datos_ave["classHierarchy"] = aves_diccionario.get("hierarchy")[0].get("classHierarchy")
        datos_ave["order"] = aves_diccionario.get("hierarchy")[0].get("order")
        datos_ave["family"] = aves_diccionario.get("hierarchy")[0].get("family")
        datos_ave["genus"] = aves_diccionario.get("hierarchy")[0].get("genus")

        #cambia los datos del ave en el valor correspondiente a la llave id 'valor'
        #ave[valor] = datos_ave

        #actualiza los datos del ave en la lista
        #aves[indice] = ave


    else:
        print(f"Por favor validar la solicitud {response.status_code}")

limpiar_pantalla()
#print(aves)

#escribir datos del diccionario en archivo datos.json
with open(nombre_archivo,"w") as archivo:
    json.dump(aves, archivo, indent=4)

print(f"El archivo JSON '{nombre_archivo}' ha sido creado correctamente.")


