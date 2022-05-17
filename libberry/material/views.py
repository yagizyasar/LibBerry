from cgitb import html
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import redirect, render
from user.models import *
from django.views.decorators.csrf import csrf_exempt
from .dataaccess import *
import datetime
# Create your views here.
def init_view(request):
    return_dict = db_get_all_mats()

    return render(request,'materials.html',{"materials":return_dict})

def add_material_root_view(request):
    return render(request,'addmaterial.html')

def add_material(request):
    if not request.user.is_authenticated:
        print("Invalid add material request: User not authenticated")
        return redirect('login')
    
    if request.session["user_type"] != "librarian":
        print("Invalid add material request: Authenticated user is not librarian")
        return redirect(request.META.get('HTTP_REFERER'))

    if request.method != "POST":
        print("Invalid add material request: Request type is not POST")
        return redirect(request.META.get('HTTP_REFERER'))

    mat_id = request.POST["mat_id"]
    title = request.POST["title"]
    genre = request.POST["genre"]
    publish_date = request.POST["publish_date"]
    amount = request.POST["amount"]
    location = request.POST["location"]
    type = request.POST["mat_type"]
    author_ids = request.POST["author_ids"]

    print(author_ids)

    if None in [mat_id, title, genre, publish_date, amount, location, type, author_ids]:
        print("Invalid add material request: Missing field in material")
        return HttpResponse("<h1> Invalid or Empty Type </h1>")
    
    match type:
        case "printed":
            pages = request.POST["pages"]
            if pages == None:
                print("Invalid add material request: Missing field in printed material")
                return HttpResponse("<h1> Invalid or Empty pages </h1>")
            db_add_material_printed(mat_id=mat_id, title=title, genre=genre, publish_date=publish_date, amount=amount, location=location, pages=pages, author_ids=author_ids)
            print("Added printed material \"{}\"".format(title))
        case "audiovisual":
            external_rating = request.POST["external_rating"]
            length = request.POST["length"]
            if external_rating == None or length == None:
                print("Invalid add material request: Missing field in audiovisual")
                return
            db_add_material_audiovisual(mat_id=mat_id, title=title, genre=genre, publish_date=publish_date, amount=amount, location=location, external_rating=external_rating, length=length, author_ids=author_ids)
            print("Added audiovisual material \"{}\"".format(title))
        case "periodical":
            pages = request.POST["pages"]
            period = request.POST["period"]
            if pages == None or period == None:
                print("Invalid add material request: Missing field in periodical")
                return
            db_add_material_periodical(mat_id=mat_id, title=title, genre=genre, publish_date=publish_date, amount=amount, location=location, pages=pages, period=period, author_ids=author_ids)
            print("Added periodical material \"{}\"".format(title))
    return redirect('root_material_view')
            
def remove_material(request):
    if not request.user.is_authenticated:
        print("Invalid remove material request: User not authenticated")
        return redirect('login')
    
    if request.session["user_type"] != "librarian":
        print("Invalid remove material request: Authenticated user is not librarian")
        return redirect(request.META.get('HTTP_REFERER'))

    if request.method != "POST":
        print("Invalid remove material request: Request type is not POST")
        return redirect(request.META.get('HTTP_REFERER'))

    mat_id = request.POST["mat_id"]
    amount = request.POST["amount"]

    if mat_id == None or amount == None:
        print("Invalid remove material request: Missing field")
        return

    db_remove_material(mat_id, amount)
    return redirect('remove_material')

def search_material(request):
    if not request.user.is_authenticated:
        print("Invalid remove material request: User not authenticated")
        return redirect('login')
    if request.method != "POST":
        print("Invalid request method for search parameters.")
        return redirect(request.META.get('HTTP_REFERER'))
    
    title = request.POST["title"]
    author_list = request.POST["author"]
    if author_list == "" or author_list == None:
        author_list = []
    if len(author_list) != 0:
        author_list = author_list.split()

    published_date = request.POST["date"]
    genre = request.POST["genre"]
    set = request.POST["set"]
    if set == "":
        set = None
    if set != None and set != "":
        set = set.split()
    rating = request.POST["rating_threshold"]
    if(rating == None or rating == ""):
        rating = 0
    rating = float(rating) / 10.0

    if(published_date == None or published_date == ""):
        published_date = "1000-01-01"
    print(author_list)
    params = {"title":title,"author":author_list,"published_after":published_date,"genre":genre,"set":set,"rating_threshold":rating}
    return_dict = db_generate_find_mat_query(params)
    return render(request,'materials.html',{"materials":return_dict})

def material_set_init_view(request):
    if not request.user.is_authenticated:
        print("Invalid remove material request: User not authenticated")
        return redirect('login')

    if request.session["user_type"] != "instructor":
        print("Invalid add material request: Authenticated user is not librarian")
        return redirect('home')
    
    course_object = db_get_all_courses_of_instructor(request.user.username)
    material_set_ids = db_get_all_sets_of_instructor(request.user.username)
    context = {"material_sets":material_set_ids,"courses":course_object}
    return render(request,'materialset.html',context)

def add_material_set(request):
    if not request.user.is_authenticated:
        print("Invalid remove material request: User not authenticated")
        return redirect('login')

    if (request.method != "POST"):
        print("Invalid request method for search parameters.")
        return redirect(request.META.get('HTTP_REFERER'))

    if request.session["user_type"] != "instructor":
        print("Invalid add material request: Authenticated user is not librarian")
        return redirect(request.META.get('HTTP_REFERER'))

    set_name = request.POST["set_name"]
    set_publicity = request.POST["set_publicity"]
    course  = request.POST["course"]
    material_list = request.POST["material_list"]
    if material_list == None or material_list == "":
        material_list = []
    else:
        material_list = material_list.split()
    db_add_material_set(request.user.username,set_publicity,set_name)
    db_add_materials_to_material_set(set_name,material_list)
    return redirect('material_set_root_view')

def remove_material_set_view(request):
    if not request.user.is_authenticated:
        print("Invalid remove material request: User not authenticated")
        return redirect('login')
    
    if request.session["user_type"] != "instructor":
        print("Invalid add material request: Authenticated user is not librarian")
        return redirect('home')
    set_id = request.POST["set-id"]
    #check koy
    db_remove_material_set(set_id)
    return redirect(request.META.get('HTTP_REFERER'))

def make_hold_request(request):
    if not request.user.is_authenticated:
        print("Invalid remove material request: User not authenticated")
        return redirect('login')
    else:
        mat_id = request.POST["mat_id"]
        user_id = request.user.username
        text = request.POST["request-text"]
        db_send_hold_request(user_id,mat_id,text)
        return redirect(request.META.get('HTTP_REFERER'))
    

    
    


    

        