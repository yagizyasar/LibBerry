from django.shortcuts import render
from .dataaccess import *
from material.dataaccess import db_get_reservation_requests
# Create your views here.

def init_warning_list_view(request):
    if request.user.is_authenticated and request.method == "GET" and request.session["user_type"] == "librarian":
       context = db_get_reservation_requests("borrowed")
       print(context)
       return render(request,'warningcreation.html',{"reservation_list":context})
    else:
        return redirect('home')

def create_overdue_warning(request):
     if request.user.is_authenticated and request.method == "POST" and request.session["user_type"] == "librarian":
        user_id = request.POST["user_id"]
        message = request.POST["text"]
        librarian_id = request.user.username
        mat_id = request.POST["mat_id"]
        debt = request.POST["balance"]
        db_send_overdue_warning(message,user_id,librarian_id,mat_id,debt)
        return redirect(request.META.get('HTTP_REFERER'))
     else:
        return redirect('home')

def create_neardue_warning(request):
    if request.user.is_authenticated and request.method == "POST" and request.session["user_type"] == "librarian":
        user_id = request.POST["user_id"]
        message = request.POST["text"]
        librarian_id = request.user.username
        mat_id = request.POST["mat_id"]
        remaing_days = request.POST["remaining_days"]
        db_send_neardue_warning(message,user_id,librarian_id,mat_id,remaing_days)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('home')

def get_all_warnings_user(request):
    if not request.user.is_authenticated:
        print("User not authenticated")
        return redirect('home')

    user_id = request.user.username

    overdue = db_get_user_overdue_warnings(user_id)
    near_due = db_get_user_near_due_warnings(user_id)
    return render(request,'warning.html',{"user_overdue_warnings":overdue, "user_near_due_warnings":near_due})