from django.urls import path
from . import views

urlpatterns = [
    path("registro", views.registro, name="maestros-registro"),
    path("", views.maestros, name="maestros"),
    path("<int:numEmpleado>", views.detalle_maestro, name="detalle-maestro"),
    path("eliminar/<int:numEmpleado>", views.eliminar_maestro, name="eliminar-maestro"),
]