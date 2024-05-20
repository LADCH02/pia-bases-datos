from django.db import connection
from django.shortcuts import redirect, render
from django.urls import reverse
from util.bd import lista_alumnos_a_diccionarios

# Create your views here.

def registro(request):
    if request.method == "GET":
        return render(request, "alumnos/registro.html")
    if request.method == "POST":
        matricula = request.POST['matricula']
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
                INSERT INTO Alumnos (Matricula, Nombre, Apellidos, Correo, Celular, IdCarrera, Semestre, Grupo)
                VALUES (%s, %s, %s, %s, %s, (SELECT IdCarrera FROM Carreras WHERE Nombre = %s), %s, (SELECT IdGrupo FROM Grupos WHERE Nombre = %s))
            """, (matricula, nombre, apellidoP + " "+ apellidoM, correo, celular, carrera, semestre, grupo))
            connection.commit()
        except Exception as e:
            connection.rollback()
            return render(request, 'alumnos/registro.html', {'error': str(e)})
        finally:
            connection.close()

        return redirect(reverse("alumnos"))

def alumnos(request):
    if request.method == "GET":
        cursor = connection.cursor()
        cursor.execute("""
            EXEC MostrarTodosAlumnos
        """)
        alumnos = cursor.fetchall()
        connection.close()
        
        alumnos_dicc = lista_alumnos_a_diccionarios(alumnos)

        return render(request, 'alumnos/index.html', {'alumnos': alumnos_dicc})

def alumnos_filtrados(request):
    if request.method == "GET":
        carrera = request.GET["carrera"]
        semestre = request.GET["semestre"]
        
        cursor = connection.cursor()
        cursor.execute("""
            EXEC MostrarAlumnosPorCarreraYSemestre @CarreraNombre=%s, @Semestre=%s
        """, [carrera, semestre])
        alumnos = cursor.fetchall()
        connection.close()
        
        alumnos_dicc = lista_alumnos_a_diccionarios(alumnos)

        return render(request, 'alumnos/index.html', {'alumnos': alumnos_dicc})
    
def alumno_especifico(request):
    matricula = request.GET["matricula"]
    return redirect('detalle-alumno', matricula=matricula)

    
def detalle_alumno(request, matricula):
    if request.method == "GET":
        cursor = connection.cursor()
        cursor.execute("""
            MostrarAlumnoPorMatricula @Matricula = %s
        """, [matricula])
        alumnos = cursor.fetchall()
        connection.close()
        
        alumno = lista_alumnos_a_diccionarios(alumnos)[0]
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
    
def eliminar_alumno(request, matricula):
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM Alumnos WHERE Matricula = %s", [matricula])
        connection.commit()
    except Exception as e:
        connection.rollback()
        return render(request, 'alumnos/detalle-alumno.html', {'error': str(e)})
    finally:
        connection.close()

    return redirect(reverse("alumnos"))