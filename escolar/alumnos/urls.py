from django.urls import path
from . import views

urlpatterns = [
    path("registro", views.registro, name="alumnos-registro"),
    path("", views.alumnos, name="alumnos"),
]