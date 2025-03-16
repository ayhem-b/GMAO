from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout

# Create your views here.
def admin(request):
    return render(request, "users/admin.html")

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users/login.html")
    else:
        form = UserCreationForm()
    return render(request, "users/register.html", {"form": form})

def user_login(request):  # I Renamed the function to avoid conflict with built-in login function
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)  # I Used auth_login instead of login 
            if user.is_superuser:
                return redirect("users:admin")
            else:
                return redirect("users:register")         
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})

def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect("users:login")