from django.shortcuts import render

# Create your views here.
def init_homework_view(request):
    if request.user.is_authenticated and request.method == "GET":
        return render(request,'homework.html')
    else:
        return render('user_login')
#def add_material_set_to_homework(request):
    