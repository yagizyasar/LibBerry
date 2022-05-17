from django.urls import path
from . import views

urlpatterns = [
    path('', views.init_warning_list_view, name='warning_creation_root'),
    path('warningoverduecreation/', views.create_overdue_warning, name='create_overdue_warning'),
    path('warningnearduecreation/',views.create_neardue_warning,name='create_nearlydue_warning')
]