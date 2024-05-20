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
    matricula = request.GET["matricula"]
    return redirect('detalle-alumno', matricula=matricula)

def detalle_grupo(request, matricula):
    if request.method == "GET":
        cursor = connection.cursor()
        cursor.execute("""
            MostrarAlumnoPorMatricula @Matricula = %s
        """, [matricula])
        alumnos = cursor.fetchall()
        connection.close()
        
        alumno = lista_grupos_a_diccionarios(alumnos)[0]
        cantidad_apellidos = len(alumno["apellidos"].split(" "))
        if cantidad_apellidos == 1:
            alumno["apellidoP"] = alumno["apellidos"]
        if cantidad_apellidos > 1:
            apellidoP, apellidoM = alumno["apellidos"].split(" ")[:2]
            alumno["apellidoP"] = apellidoP
            alumno["apellidoM"] = apellidoM
        
        return render(request, "alumnos/detalle-alumno.html", {'alumno': alumno})

    if request.method == "POST":
        matriculaNueva = request.POST['matricula']
        nombre = request.POST['nombre']
        apellidoP = request.POST['apellidoP']
        apellidoM = request.POST['apellidoM']
        correo = request.POST['correo']
        celular = request.POST['celular']
        grupo = request.POST['grupo']
        carrera = request.POST['carrera']
        semestre = request.POST['semestre']
        
        cursor = connection.cursor()

        try:
            cursor.execute("""
                UPDATE Alumnos
                SET Matricula = %s,
                    Nombre = %s,
                    Apellidos = %s,
                    Correo = %s,
                    Celular = %s,
                    IdCarrera = (SELECT IdCarrera FROM Carreras WHERE Nombre = %s),
                    Semestre = %s,
                    Grupo = (SELECT IdGrupo FROM Grupos WHERE Nombre = %s)
                WHERE Matricula = %s
            """, (matriculaNueva, nombre, apellidoP + " " + apellidoM, correo, celular, carrera, semestre, grupo, matricula))
            connection.commit()
        except Exception as e:
            connection.rollback()
            return render(request, 'alumnos/detalle-alumno.html', {'error': str(e)})
        finally:
            connection.close()

        return redirect(reverse("alumnos"))
