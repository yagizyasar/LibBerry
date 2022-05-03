from django.shortcuts import render
from user.models import *


def login():
    return

def register(request):
    if not request.user.is_authenticated:
        print("Invalid register request: Librarian not authenticated")
        return

    if request.method != "POST":
        print("Invalid register request: Request must be POST")
        return

    type = request.POST["type"]
    if type not in ["student", "instructor", "librarian", "outside_member"]:
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
   #db_register_user(user=user, balance=0, registrar_id=request.user.username)
    match type:
        case "student":
            gpa = request.POST["gpa"]
            department = request.POST["department"]

            if gpa == None or department == None:
                print("Invalid register request: Missing field in Student")
                return
            #db_register_student(user=user, department=department, gpa=gpa)
            return
        case "instructor":
            office = request.POST["office"]
            department = request.POST["department"]

            if office == None or department == None:
                print("Invalid register request: Missing field in Instructor")
                return
            #db_register_instructor(user=user, department=department, gpa=gpa)
            return
        case "librarian":
            spec = request.POST["specialization"]
            
            if spec == None:
                print("Invalid register request: Missing field in Librarian")
                return
            #db_register_librarian(user=user, specialization=spec)
            return
        case "outside_member":
            reg_date = request.POST["registration_date"]
            card_no = request.POST["card_no"]
            expire_date = request.POST["expire_date"]

            if reg_date == None or card_no == None or expire_date == None:
                print("Invalid register request: Missing field in OutsideMember")
                return
            #db_register_outside_member(user=user, registration_date=reg_date, card_no=card_no, expire_date=expire_date)
            return

