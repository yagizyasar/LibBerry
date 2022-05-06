from cgitb import html
from os import remove
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import redirect, render
from user.models import *
from django.views.decorators.csrf import csrf_exempt
from .dataaccess import *
from django.http import HttpResponseRedirect

def init_view(request):
    return render(request,'login.html')

def fetch_all_users_view(request):
    if request.user.is_authenticated and request.method == "GET" and request.session["user_type"] == "librarian":
        users = get_all_users()
        return render(request,'registration.html',{'users':users})
    
    return redirect('home')



def user_login(request):
    if request.user.is_authenticated:
        print("Invalid login request: User already authenticated")

    if request.method != "POST":
        print("Invalid login request: Request must be GET")
        return

    username = request.POST['user-id']
    password = request.POST['user-password']

    if username == None or password == None:
        print("Invalid login request: Missing username or password field")
        return

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request,user)
        print("User logged in")
        request.session["user_type"] = get_user_type(user.username)
        # TODO save more variables if needed
        return redirect('home')
        # TODO redirect page i gelince yolla
    else:
        print("Invalid login request: Wrong username or password")
        # TODO adama error ver

@csrf_exempt
def user_register(request):
    if not request.user.is_authenticated:
        print("Invalid register request: Librarian not authenticated")
        return redirect('user_login')

    if request.session["user_type"] != "librarian":
        print("Invalid Permissions for registration")
        return redirect('home')
        
    if request.method != "POST":
        print("Invalid register request: Request must be POST")
        return

    type = request.POST["type"]
    if type not in ["student", "instructor", "librarian", "outsidemember"]:
        print("Invalid register request: Invalid user type in request")
        return

    # register form main fields (django)
    uni_id = request.POST["id"]
    password = request.POST["password"]
    email = request.POST["email"]
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    
    if uni_id == None or password == None or email == None or first_name == None or last_name == None:
        print("Invalid register request: Missing field in User")
        return
        
    user = User.objects.create_user(username=uni_id, password=password,email=email)
    user.first_name = first_name
    user.last_name = last_name
    user.save()

    # type specific updates
    db_register_mainuser(username=user.username, balance=0, registrar_id=request.user.username,type=type)
    match type:
        case "student":
            gpa = request.POST["gpa"]
            department = request.POST["department"]

            if gpa == None or department == None:
                print("Invalid register request: Missing field in Student")
                return
            db_register_student(user=user, department=department, gpa=gpa)
            print("Registered student")
            return redirect("register_panel")
        case "instructor":
            office = request.POST["office"]
            department = request.POST["department"]
            tenure = request.POST["tenure"]
            if office == None or department == None or tenure == None:
                print("Invalid register request: Missing field in Instructor")
                return
            db_register_instructor(user=user, office=office, department=department,tenure=tenure)
            print("Registered instructor")
            return redirect("register_panel")
        case "librarian":
            spec = request.POST["specialization"]
            
            if spec == None:
                print("Invalid register request: Missing field in Librarian")
                return
            db_register_librarian(user=user, specialization=spec)
            print("Registered librarian")
            return redirect("register_panel")
        case "outsidemember":
            #reg_date = request.POST["registration_date"]
            card_no = request.POST["card_no"]
            expire_date = request.POST["expire_date"]

            if card_no == None or expire_date == None:
                print("Invalid register request: Missing field in OutsideMember")
                return
            db_register_outside_member(user=user, card_no=card_no, expire_date=expire_date)
            print("Registered outside member")
            return redirect("register_panel")

def user_remove(request):
    if not request.user.is_authenticated:
        print("Invalid register request: Librarian not authenticated")
        return redirect('user_login')
    
    if request.session["user_type"] != "librarian":
        print("Invalid Permissions for deletion")
        return redirect('home')
    
    if request.method != "POST":
        print("Invalid deletion request: Request must be POST")
        return HttpResponseRedirect(request.path_info)
    
    deleted_user = request.post["username"]
    if deleted_user:
        remove_user(deleted_user)
        print("Registered outside member")
    else:
        print("Username to delete is NULL")
    return redirect("register_panel")

    
        
    

            

