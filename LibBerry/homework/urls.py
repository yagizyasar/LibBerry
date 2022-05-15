from django.urls import path
from . import views

urlpatterns = [
    path('',views.init_homework_view,name='init_homework')
]