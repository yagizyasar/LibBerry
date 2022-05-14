from cgitb import html
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import redirect, render
from user.models import *
from django.views.decorators.csrf import csrf_exempt
from .dataaccess import *

# Create your views here.
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

    if None in [mat_id, title, genre, publish_date, amount, location, type, author_ids]:
        print("Invalid add material request: Missing field in material")
        return
    
    match type:
        case "printed":
            pages = request.POST["pages"]
            if pages == None:
                print("Invalid add material request: Missing field in printed material")
                return
            db_add_material_printed(mat_id=mat_id, title=title, genre=genre, publish_date=publish_date, amount=amount, location=location, pages=pages, author_ids=author_ids)
            print("Added printed material \"{1}\"".format(title))
            return redirect('add_material')
        case "audiovisual":
            external_rating = request.POST["external_rating"]
            length = request.POST["length"]
            if external_rating == None or length == None:
                print("Invalid add material request: Missing field in audiovisual")
                return
            db_add_material_audiovisual(mat_id=mat_id, title=title, genre=genre, publish_date=publish_date, amount=amount, location=location, external_rating=external_rating, length=length, author_ids=author_ids)
            print("Added audiovisual material \"{1}\"".format(title))
            return redirect('add_material')
        case "periodical":
            pages = request.POST["pages"]
            period = request.POST["period"]
            if pages == None or period == None:
                print("Invalid add material request: Missing field in periodical")
                return
            db_add_material_periodical(mat_id=mat_id, title=title, genre=genre, publish_date=publish_date, amount=amount, location=location, pages=pages, period=period, author_ids=author_ids)
            print("Added periodical material \"{1}\"".format(title))
            return redirect('add_material')
            
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


    

        