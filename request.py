#1 uso de requests para consumir datos de una web o de un ws
import json
import requests
from funciones_captura import limpiar_pantalla

# Nombre del archivo JSON de salida
nombre_archivo = "hongos_cundinamarca.json"

#2 definir una url para consumir o consultar
#url = "https://api.catalogo.biodiversidad.co/record_search/advanced_search?class=Aves&department=CO-BOY&size=300"



url = "https://api.catalogo.biodiversidad.co/record_search/advanced_search?kingdom=fungi&department=CO-CUN&size=200"

#url = "https://api.catalogo.biodiversidad.co/record_search/advanced_search?kingdom=animalia&department=CO-BOY&size=58"
#url = "https://api.catalogo.biodiversidad.co/record_search/advanced_search?kingdom=fungi&department=CO-CUN&size=200"

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

        #(cambio) anezamos el id del registro a los datos
        datos_ave["_id"] = datos.get("_id")
        
        #leo y almaceno en el diccionario 'datos_ave' la información general de cada una de las aves
        try:
            datos_ave["exotic"]= datos.get("originAtomized").get("exotic")
        except:
            datos_ave["exotic"]= ""

        try:     
            datos_ave["invasive"] = datos.get("originAtomized").get("invasive")
        except:
            datos_ave["invasive"] = ""

        try:
            datos_ave["name_scientific"] = datos.get('taxonRecordNameApprovedInUse').get("taxonRecordName").get("scientificName").get("canonicalName").get("simple")
        except:
            datos_ave["name_scientific"] = ""

        try:
            datos_ave["name_common"] = datos.get('commonNames')[0].get("name")
        except:
            datos_ave["name_common"] = ""
        try:
            datos_ave["names"] = datos.get('commonNames')
        except:
            datos_ave["names"] = ""

        try:
            datos_ave["general_desc"] = datos.get("fullDescriptionApprovedInUse").get("fullDescription").get("fullDescriptionUnstructured")
        except:
            datos_ave["general_desc"] = ""

        try:
            datos_ave["img_main"] = datos.get("imageInfo").get("mainImage")
        except:
            datos_ave["img_main"] = ""

        try:
            datos_ave["img_thumbnail"] = datos.get("imageInfo").get("thumbnailImage")
        except:
            datos_ave["img_thumbnail"] = ""

        #agrega a cada id, los datos del ave
        #ave[datos.get("_id")] = datos_ave

        #agrero cada una de las aves al listado 'aves'
        aves.append(datos_ave)

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
    
        #obtengo el diccionario con el id y contenido del ave
        #ave = aves[indice]

        #obtengo los datos del ave a partir de su id
        #datos_ave = ave.get(valor)
        datos_ave = aves[indice]
        try:
            datos_ave["reproduction"] = aves_diccionario.get("reproductionApprovedInUse").get("reproduction").get("reproductionUnstructured")
        except:
            datos_ave["reproduction"] = ""
        
        try:
            datos_ave["distribution"] = aves_diccionario.get("distributionApprovedInUse").get("distribution")[0].get("distributionUnstructured")
        except:
            datos_ave["distribution"] = ""
        
        try:
            datos_ave["abstract"] = aves_diccionario.get("abstractApprovedInUse").get("abstract")
        except:
            datos_ave["abstract"] =""
        
        try:
            datos_ave["feeding"] = aves_diccionario.get("feedingApprovedInUse").get("feeding").get("feedingUnstructured")
        except:
            datos_ave["feeding"] = ""
        
        try:
            datos_ave["behavior"] = aves_diccionario.get("behaviorApprovedInUse").get("behavior").get("behaviorUnstructured")
        except:
            datos_ave["behavior"] = ""

        try:
            datos_ave["habitats"] = aves_diccionario.get("habitatsApprovedInUse").get("habitats").get("habitatUnstructured")
        except:
            datos_ave["habitats"] = ""

        try:            
            datos_ave["kingdom"] = aves_diccionario.get("hierarchy")[0].get("kingdom")
        except:
            datos_ave["kingdom"] = ""

        try:
            datos_ave["phylum"] = aves_diccionario.get("hierarchy")[0].get("phylum")
        except:
            datos_ave["phylum"] = ""
        
        try:
            datos_ave["classHierarchy"] = aves_diccionario.get("hierarchy")[0].get("classHierarchy")
        except:
            datos_ave["classHierarchy"] = ""

        try:
            datos_ave["order"] = aves_diccionario.get("hierarchy")[0].get("order")
        except:
            datos_ave["order"] = ""

        try:
            datos_ave["family"] = aves_diccionario.get("hierarchy")[0].get("family")
        except:
            datos_ave["family"] = ""

        try:
            datos_ave["genus"] = aves_diccionario.get("hierarchy")[0].get("genus")
        except:
            datos_ave["genus"] = ""

        #cambia los datos del ave en el valor correspondiente a la llave id 'valor'
        #ave[valor] = datos_ave

        #actualiza los datos del ave en la lista
        #aves[indice] = ave


    else:
        print(f"Por favor validar la solicitud {response.status_code}")

limpiar_pantalla()
#print(aves)

#escribir datos del diccionario en archivo datos.json
with open(nombre_archivo,"w",encoding="utf8") as archivo:
    json.dump(aves, archivo, indent=4)

print(f"El archivo JSON '{nombre_archivo}' ha sido creado correctamente.")
print(f"Cantidad de especimenes : {len(aves)}")

