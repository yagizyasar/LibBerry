from django.urls import path
from . import views

urlpatterns = [
    path('',views.init_homework_view,name='init_homework'),
    path('createhomework/',views.create_homework,name='create_homework'),
    path('homeworktocourse/',views.add_homework_to_course,name='course_homework'),
    path('homeworktostudent/',views.add_homework_to_student,name='student_homework'),
    path('coursecreationandstudent/',views.register_student_or_course_root,name='course_register_root'),
    path('registerstudentocourse/',views.register_student_to_course,name='register_student_course'),
    path('registercourse/',views.register_course,name='create_course'),
]