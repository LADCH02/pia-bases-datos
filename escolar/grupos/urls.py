from django.urls import path
from . import views

urlpatterns = [
    path("", views.grupos, name="grupos"),
    path("especifico", views.grupo_especifico, name="grupo-especifico"),
    path("<int:matricula>", views.detalle_grupo, name="detalle-grupo"),
]