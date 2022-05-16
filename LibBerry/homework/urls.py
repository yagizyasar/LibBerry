from django.urls import path
from . import views

urlpatterns = [
    path('',views.init_homework_view,name='init_homework'),
    path('createhomework/',views.create_homework,name='create_homework'),
    path('homeworktocourse/',views.add_homework_to_course,name='course_homework'),
    path('homeworktostudent/',views.add_homework_to_student,name='student_homework'),


]