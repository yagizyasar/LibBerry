from django.urls import path
from . import views

urlpatterns = [
    path('', views.init_warning_list_view, name='warning_creation_root'),
    path('warningcreation/', views.create_warning, name='warning_creation'),
]