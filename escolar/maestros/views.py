from django.db import connection
from django.shortcuts import redirect, render
from django.urls import reverse
from util.bd import lista_maestros_a_diccionarios

# Create your views here.

def registro(request):
    if request.method == "GET":
        return render(request, "maestros/registro.html")
    if request.method == "POST":
        numEmpleado = request.POST['numEmpleado']
        nombre = request.POST['nombre']
        apellidoP = request.POST['apellidoP']
        apellidoM = request.POST['apellidoM']
        correo = request.POST['correo']
        celular = request.POST['celular']
        grupo = request.POST['grupo']
        
        cursor = connection.cursor()

        try:
            cursor.execute("""
                INSERT INTO Maestros (NumEmpleado, Nombre, Apellidos, Correo, Celular, Grupo)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (numEmpleado, nombre, apellidoP + " " + apellidoM, correo, celular, grupo))
            connection.commit()
        except Exception as e:
            connection.rollback()
            return render(request, 'maestros/registro.html', {'error': str(e)})
        finally:
            connection.close()

        return redirect(reverse("maestros"))

def maestros(request):
    if request.method == "GET":
        cursor = connection.cursor()
        cursor.execute("""
            SELECT NumEmpleado, Nombre, Apellidos, Correo, Celular, Grupo
            FROM Maestros
        """)
        maestros = cursor.fetchall()
        connection.close()
        
        alumnos_dicc = lista_maestros_a_diccionarios(maestros)

        return render(request, 'maestros/index.html', {'maestros': alumnos_dicc})
    
def detalle_maestro(request, numEmpleado):
    if request.method == "GET":
        cursor = connection.cursor()
        cursor.execute("""
            SELECT NumEmpleado, Nombre, Apellidos, Correo, Celular, Grupo
            FROM Maestros WHERE NumEmpleado = %s
        """, [numEmpleado])
        maestros = cursor.fetchall()
        connection.close()
        
        maestro = lista_maestros_a_diccionarios(maestros)[0]
        cantidad_apellidos = len(maestro["apellidos"].split(" "))
        if cantidad_apellidos == 1:
            maestro["apellidoP"] = maestro["apellidos"]
        if cantidad_apellidos > 1:
            apellidoP, apellidoM = maestro["apellidos"].split(" ")[:2]
            maestro["apellidoP"] = apellidoP
            maestro["apellidoM"] = apellidoM
        
        return render(request, "maestros/detalle-maestro.html", {'maestro': maestro})

    if request.method == "POST":
        numEmpleadoNuevo = request.POST['numEmpleado']
        nombre = request.POST['nombre']
        apellidoP = request.POST['apellidoP']
        apellidoM = request.POST['apellidoM']
        correo = request.POST['correo']
        celular = request.POST['celular']
        grupo = request.POST['grupo']
        
        cursor = connection.cursor()

        try:
            cursor.execute("""
                UPDATE Maestros
                SET NumEmpleado = %s,
                    Nombre = %s,
                    Apellidos = %s,
                    Correo = %s,
                    Celular = %s,
                    Grupo = %s
                WHERE NumEmpleado = %s
            """, (numEmpleadoNuevo, nombre, apellidoP + " " + apellidoM, correo, celular, grupo, numEmpleado))
            connection.commit()
        except Exception as e:
            connection.rollback()
            return render(request, 'maestros/detalle-maestro.html', {'error': str(e)})
        finally:
            connection.close()

        return redirect(reverse("maestros"))
    
def eliminar_maestro(request, numEmpleado):
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM Maestros WHERE numEmpleado = %s", [numEmpleado])
        connection.commit()
    except Exception as e:
        connection.rollback()
        return render(request, 'maestros/detalle-maestro.html', {'error': str(e)})
    finally:
        connection.close()

    return redirect(reverse("maestros"))