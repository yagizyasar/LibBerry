from django.urls import path
from . import views

urlpatterns = [
    path('addmaterialrequest/', views.add_material, name='add_material_request'),
    path('removematerial/', views.remove_material, name='remove_material'),
    path('removematerialset/', views.remove_material_set_view, name='material_set_remove'),
    path('',views.init_view,name='root_material_view'),
    path('search/',views.search_material,name='search'),
    path('materialset/',views.material_set_init_view,name='material_set_root_view'),
    path('addmaterial/',views.add_material_root_view,name='add_material')
]