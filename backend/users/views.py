from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
# Create your views here.  
def admin(request):
    return render(request,"users/admin.html")
 
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users/login.html")
    else:
        form = UserCreationForm()
    return render(request,"users/register.html",{"form":form}) 

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            return redirect("users:admin")

    else:
        form = AuthenticationForm()
    return render(request,"users/login.html",{"form":form})