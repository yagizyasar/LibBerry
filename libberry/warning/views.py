from django.shortcuts import render
from .dataaccess import *
from material.dataaccess import db_get_reservation_requests
# Create your views here.

def init_warning_list_view(request):
    if request.user.is_authenticated and request.method == "GET" and request.session["user_type"] == "librarian":
       context = db_get_reservation_requests("borrowed")
       return render(request,'warningcreation.html',{"reservation_list":context})
    else:
        return redirect('home')
