from django.urls import path
from . import views

urlpatterns = [
    path('addmaterial/', views.add_material, name='add_material'),
    path('removematerial/', views.remove_material, name='remove_material'),
    path('',views.init_view,name='root_material_view'),
    path('search/',views.search_material,name='search')
]