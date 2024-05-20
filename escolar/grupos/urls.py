from django.urls import path
from . import views

urlpatterns = [
    path("", views.grupos, name="grupos"),
    path("especifico", views.grupo_especifico, name="grupo-especifico"),
    path("grupo/<str:grupoNombre>", views.detalle_grupo, name="detalle-grupo"),
]