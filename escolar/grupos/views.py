from django.db import connection
from django.shortcuts import redirect, render
from django.urls import reverse
from util.bd import lista_grupos_a_diccionarios, lista_data_a_diccionarios

# Create your views here.

def grupos(request):
    if request.method == "GET":
        cursor = connection.cursor()
        cursor.execute("""
            EXEC MostrarTodosGrupos
        """)
        grupos = cursor.fetchall()
                
        grupos_dicc = lista_grupos_a_diccionarios(grupos)
        
        for grupo in grupos_dicc:
            grupo["alumnos"] = []
            grupo["maestros"] = []
            # obtener alumnos del grupo
            cursor.execute(
                """SELECT Matricula, Nombre, Apellidos FROM Alumnos WHERE Grupo = %s""", 
                [grupo["nombre"]]
            )
            alumnos = lista_data_a_diccionarios(cursor.fetchall(), ["matricula", "nombre", "apellidos"])
            grupo["alumnos"] += alumnos
            
            # obtener maestros del grupo
            cursor.execute(
                """SELECT NumEmpleado, Nombre, Apellidos FROM Maestros WHERE Grupo = %s""", 
                [grupo["nombre"]]
            )
            maestros = lista_data_a_diccionarios(cursor.fetchall(), ["numEmpleado", "nombre", "apellidos"])
            grupo["maestros"] += maestros
            
        connection.close()

        return render(request, 'grupos/index.html', {'grupos': grupos_dicc})

def grupo_especifico(request):
    grupo = request.GET["grupo"]
    return redirect('detalle-grupo', grupoNombre=grupo)

def detalle_grupo(request, grupoNombre):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT IdGrupo, Nombre FROM Grupos WHERE Nombre = %s
    """, [grupoNombre])
    grupos = cursor.fetchall()

    grupos_dicc = lista_grupos_a_diccionarios(grupos) # solo retorna un grupo
    grupo = grupos_dicc[0]
    
    grupo["alumnos"] = []
    grupo["maestros"] = []
    # obtener alumnos del grupo
    cursor.execute(
        """SELECT Matricula, Nombre, Apellidos FROM Alumnos WHERE Grupo = %s""", 
        [grupo["nombre"]]
    )
    alumnos = lista_data_a_diccionarios(cursor.fetchall(), ["matricula", "nombre", "apellidos"])
    grupo["alumnos"] += alumnos
    
    # obtener maestros del grupo
    cursor.execute(
        """SELECT NumEmpleado, Nombre, Apellidos FROM Maestros WHERE Grupo = %s""", 
        [grupo["nombre"]]
    )
    maestros = lista_data_a_diccionarios(cursor.fetchall(), ["numEmpleado", "nombre", "apellidos"])
    grupo["maestros"] += maestros
    
    return render(request, "grupos/detalle-grupo.html", {'grupo': grupo})

