def lista_data_a_diccionarios(datas, llaves):
    datas_dict_list = []
    for data in datas:
        data_dict = {}
        for i, valor in enumerate(data):
            data_dict[llaves[i]] = valor
        datas_dict_list.append(data_dict)
    return datas_dict_list

def lista_alumnos_a_diccionarios(alumnos):
    llaves = ['matricula', 'nombre', 'apellidos', 'correo', 'celular', 'carrera', 'semestre', 'grupo']
    return lista_data_a_diccionarios(alumnos, llaves)

def lista_maestros_a_diccionarios(maestros):
    llaves = ['numEmpleado', 'nombre', 'apellidos', 'correo', 'celular', 'grupo', 'grupoNombre']
    return lista_data_a_diccionarios(maestros, llaves)

def lista_grupos_a_diccionarios(grupos):
    llaves = ['id', 'nombre']
    return lista_data_a_diccionarios(grupos, llaves)
