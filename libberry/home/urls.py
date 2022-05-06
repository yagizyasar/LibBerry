from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('',views.init_view,name='home'),
    path('registerpanel/',views.fetch_all_users_view,name='register_panel'),
    path('removeuser/',views.user_remove,name='user_remove')
]