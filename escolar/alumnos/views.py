from django.db import connection
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.messages import add_message

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

        with connection.cursor() as cursor:
            # make a valid cursor.execute
            cursor.execute("""
                INSERT INTO Alumnos (matricula, Nombre, Apellidos, Correo, Celular, IdCarrera, Semestre, Grupo)
                VALUES (%s, %s, %s, %s, %s, (SELECT IdGrupo FROM Grupos WHERE Nombre = %s), %s, (SELECT IdGrupo FROM Grupos WHERE Nombre = %s))
            """, (matricula, nombre, apellidoP + " "+ apellidoM, correo, celular, carrera, semestre, grupo))

        return redirect(reverse("inicio"))
