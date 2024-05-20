def lista_alumnos_a_diccionarios(alumnos):
    llaves = ['matricula', 'nombre', 'apellidos', 'correo', 'celular', 'carrera', 'semestre', 'grupo', 'grupoNombre']
    alumnos_dict_list = []
    for alumno in alumnos:
        alumno_dict = {}
        for i, valor in enumerate(alumno):
            alumno_dict[llaves[i]] = valor
        alumnos_dict_list.append(alumno_dict)
    return alumnos_dict_list

def lista_maestros_a_diccionarios(alumnos):
    llaves = ['numEmpleado', 'nombre', 'apellidos', 'correo', 'celular', 'grupo', 'grupoNombre']
    alumnos_dict_list = []
    for alumno in alumnos:
        alumno_dict = {}
        for i, valor in enumerate(alumno):
            alumno_dict[llaves[i]] = valor
        alumnos_dict_list.append(alumno_dict)
    return alumnos_dict_list
