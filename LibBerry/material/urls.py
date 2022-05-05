from django.urls import path
from . import views

urlpatterns = [
    path('addmaterial/', views.add_material, name='add_material'),
    path('removematerial/', views.remove_material, name='remove_material')
]