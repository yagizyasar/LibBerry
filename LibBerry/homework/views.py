from multiprocessing import context
from django.shortcuts import redirect, render
from .dataaccess import *
# Create your views here.
def init_homework_view(request):
    if request.user.is_authenticated and request.method == "GET" and request.session["user_type"] == "instructor":
        hws = db_get_all_homeworks_instructor(request.user.username)
        courses = db_get_all_courses_instructor(request.user.username)
        material_sets = db_get_all_materialsets_instructor(request.user.username)
        students = db_get_all_students_of_instructor(request.user.username)
        print(students)
        return render(request,'homework.html',{"homeworks":hws,"courses":courses,"mat_sets":material_sets,"student_section":students})
    elif request.user.is_authenticated and request.method == "GET" and request.session["user_type"] == "student":
        context = db_get_students_homeworks(request.user.username)
        return render(request,'homework.html',{"homeworks":context})
    elif not request.user.is_authenticated:
        return redirect('home')

def init_homework_2(request):
    if request.user.is_authenticated and request.method == "GET" and request.session["user_type"] == "instructor":
        hws = db_get_all_homeworks_instructor(request.user.username)
        courses = db_get_all_courses_instructor(request.user.username)
        material_sets = db_get_all_materialsets_instructor(request.user.username)
        students = db_get_all_students_of_instructor(request.user.username)
        return render(request,'homework_seperate.html',{"homeworks":hws,"courses":courses,"mat_sets":material_sets,"student_section":students})
    else:
        return redirect('home')

def create_homework(request):
    if request.user.is_authenticated and request.method == "POST" and request.session["user_type"] == "instructor":
        hw_id = request.POST["hw_id"]
        material_set_id = request.POST["material-select"]
        due = request.POST["due"]
        db_add_homework(hw_id,due,material_set_id,request.user.username)
        return redirect('init_homework')
    if not request.user.is_authenticated:
        return redirect('user_login')

def add_homework_to_course(request):
    if request.user.is_authenticated and request.method == "POST" and request.session["user_type"] == "instructor":
        hw_id = request.POST["hw_id"]
        section = request.POST["section"]
        course_id = request.POST["course_id"]
        db_give_homework_to_coursesection(course_id,section,"spring",2022,hw_id)
        return redirect('init_homework')
    if not request.user.is_authenticated:
        return redirect('user_login')

def add_homework_to_student(request):
    if request.user.is_authenticated and request.method == "POST" and request.session["user_type"] == "instructor":
        hw_id = request.POST["hw_id"]
        student_ids = request.POST["student_ids"].split()
        db_give_homework_to_student(student_ids,hw_id)
        return redirect('init_homework')
    if not request.user.is_authenticated:
        return redirect('user_login')

def register_student_to_course(request):
     if request.user.is_authenticated and request.method == "POST" and request.session["user_type"] == "librarian":
        user_id_student = request.POST["user_id_student"]
        course_id_student = request.POST["course_id_student"]
        section_student = request.POST["section_student"]
        set_semester_student = request.POST["set_semester_student"]
        year = request.POST["year_student"]
        db_add_student_to_coursesection(user_id_student,course_id_student,section_student,set_semester_student,year)
        return redirect(request.META.get('HTTP_REFERER'))


def register_course(request):
    if request.user.is_authenticated and request.method == "POST" and request.session["user_type"] == "librarian":
        course_id = request.POST["course_id"]
        section = request.POST["section"]
        set_semester = request.POST["set_semester"]
        year = request.POST["year"]
        instructor_id = request.POST["instructor_id"]
        db_add_coursesection(course_id,section,set_semester,year,instructor_id)
        return redirect(request.META.get('HTTP_REFERER'))

def register_student_or_course_root(request):
    if request.user.is_authenticated and request.method == "GET" and request.session["user_type"] == "librarian":
       courses = db_get_all_courses()
       return render(request,'courseregistration.html',{"courses":courses})
    else:
        return redirect(request.META.get('HTTP_REFERER'))


    


    