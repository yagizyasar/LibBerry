from django.urls import path
from . import views

urlpatterns = [
    path('warningcreation/', views.init_warning_list_view, name='warning_creation'),
]