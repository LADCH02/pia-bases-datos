from django.urls import path
from . import views

urlpatterns = [
    path("registro", views.registro, name="alumnos-registro"),
    path("", views.alumnos, name="alumnos"),
    path("filtrados", views.alumnos_filtrados, name="alumnos-filtrados"),
    path("especifico", views.alumno_especifico, name="alumno-especifico"),
    path("<int:matricula>", views.detalle_alumno, name="detalle-alumno"),
    path("eliminar/<int:matricula>", views.eliminar_alumno, name="eliminar-alumno"),
]