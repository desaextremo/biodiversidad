//Referencia a la lista de los departamentos
let deptos = document.querySelector("#deptos")
//Referencia a la lista de los reinos
let reinos = document.querySelector("#reinos")
//Referencia a la tabla de datos
let datos_consulta = document.querySelector("#datos_consulta")
//Referencia al boton
let boton_consultr = document.querySelector("#consultar")
//Referencia a la lista de los grupos
let listado_grupos = document.querySelector("#lista_grupos")
//Referencia a la lista de filas de la tabla de datos
let datos_filas = document.querySelector("#filas")
//variable de control
let consulta = false;
let grupos = [];
let grupo_seleccionado = 0;
let paginador = 10;


//Inicialmente la tabla de datos esta oculta
datos_consulta.style.display = "none"

listado_grupos.disabled = true;

//eventos de clic para el boton
boton_consultr.addEventListener("click", function () {
    validar_seleccion();
})

//eventos de cambio o seleccion para la lista de departamentos
deptos.addEventListener("change",function (){
    reiniciar_consulta()
})

//eventos de cambio o seleccion para la lista de reinos
reinos.addEventListener("change",function (){
    reiniciar_consulta()        
})

function reiniciar_consulta(){
    grupos = []
    consulta = false
    listado_grupos.innerHTML=""
    listado_grupos.disabled = true;
    datos_consulta.style.display = "none"
    datos_filas.innerHTML=""
    grupo_seleccionado=0
}

//funcion para el procesamiento de evento clic
//Recuperar datos, validar, y realziar la peticion
function validar_seleccion() {
    let departamento_seleccionado = parseInt(deptos.value)
    let reino_seleccionado = parseInt(reinos.value)
    let tipo_consulta = 1

    //Boyaca / Animales
    if (departamento_seleccionado === 1 && reino_seleccionado == 1)
        tipo_consulta = 1
    //Cundinamarca / Animales
    else if (departamento_seleccionado === 2 && reino_seleccionado == 1)
        tipo_consulta = 2
    //Boyaca / Hongos
    else if (departamento_seleccionado === 1 && reino_seleccionado == 3)
        tipo_consulta = 3
    //Cundinamarca / Hongos
    else if (departamento_seleccionado === 2 && reino_seleccionado == 3)
        tipo_consulta = 4
    //Boyaca / Plantas
    else if (departamento_seleccionado === 1 && reino_seleccionado == 2)
        tipo_consulta = 5
    //Cundinamarca / Plantas
    else if (departamento_seleccionado === 2 && reino_seleccionado == 2)
        tipo_consulta = 6


    procesar_consulta(tipo_consulta)
}

function procesar_consulta(tipo_consulta) {
    let url = "http://localhost:8080/consultar/" + tipo_consulta;
    //arreglo de especimenes
    const especimenes = [];

    let registros = 0
    let ultimo_grupo = 0
    let cantidad_grupos = 0
    let opciones_grupo = ""
    let filas = ""


    //valida si ya se ejecuto la consulta por primera vez
    if (consulta){
        //obtengo el grupo seleccionado
        grupo_seleccionado = parseInt(listado_grupos.value)

        //identifico para ese grupo seleccionado su limite inferior o inicio, y
        //su limite superior o final
        let inicio = grupos[grupo_seleccionado].inicio
        let final = grupos[grupo_seleccionado].final

        url += `/${inicio}/${final}`
    }else{
        url += `/1/${paginador}`
    }
    
    axios.get(url)
        .then(function (response) {
            data = response.data

            //recupera la cantidad de registros 
            registros = data[0].rows;


            if(registros % paginador > 0) {
                ultimo_grupo = registros % paginador;
                cantidad_grupos +=1;
            }
            cantidad_grupos += Math.trunc(registros / paginador)

            if (ultimo_grupo > 0) cantidad_grupos--;

            console.log(cantidad_grupos)
            console.log(ultimo_grupo)

            inicial=1
            final = paginador

            grupos = []
            //Construccion de cantidades de registro
            for (let i = 1; i <= cantidad_grupos; i++) {

                let grupo = {
                             "inicio": inicial,
                             "final" : final
                            }
                //adiciono el grupo al arreglo de grupos
                grupos.push(grupo)

                inicial += paginador
                final += paginador
            }

            //si hay uno ultimo grupo los agrega al arreglo de grupos de paginacion
            if (ultimo_grupo > 0)  grupos.push({"inicio": inicial,"final" : final - paginador + ultimo_grupo})
            
                
            //arma los elemento del listado
            grupos.forEach((element, index) =>{
                opciones_grupo += `<option value="${index}">${index+1}</option>`
            });

            listado_grupos.innerHTML=opciones_grupo       

            //eliminar del arreglo el objeto que contiene el toral de los registros 
            data.splice(0, 1);

            //recorrer areglo e ir creando objetos unicamente con los datos que necesito
            data.forEach(item => {

                let especimen = {
                    _id: item._id,
                    name_scientific: item.name_scientific,
                    name_common: item.name_common,
                    kingdom: item.kingdom,
                    phylum: item.phylum,
                    classHierarchy: item.classHierarchy,
                    order: item.order,
                    family: item.family,
                    genus: item.genus
                }

                especimenes.push(especimen);                
            });

            especimenes.forEach((element, index) => {
                //console.log(` Especimen ${index + 1}`)
                for (const [key, value] of Object.entries(element)) {
                    if (key=="_id"){
                        filas += `<td scope="col"><a href="${value}"><img src="../img/view.png"></a></td>`;
                    }else filas += `<td scope="col">${value}</td>`;
                }
                filas += "</tr>"
            })

            datos_filas.innerHTML=filas       
            //vuelve visible la tabla de datos
            datos_consulta.style.display = "block"     
            consulta = true
            listado_grupos.disabled = false;
            listado_grupos.value = grupo_seleccionado

        })
        .catch(function (error) {
            console.log(error)
        })
}
