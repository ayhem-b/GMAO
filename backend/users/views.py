from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib import messages 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from maintenance.models import Intervention, Machine
from maintenance.forms import InterventionForm


@login_required
def edit_user(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        first_name = request.POST.get("first_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        role = request.POST.get("role")

        try:
            user = User.objects.get(id=user_id)
            user.username = username
            user.first_name = first_name
            user.email = email

            # Update role
            if role == "Admin":
                user.is_staff = True
                user.is_superuser = True
            else:  # Role = "User"
                user.is_staff = False
                user.is_superuser = False

            user.save()
            return JsonResponse({"success": True})
        except User.DoesNotExist:
            return JsonResponse({"success": False, "error": "User not found"})
    
    return JsonResponse({"success": False, "error": "Invalid request"})
def delete_user(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")

        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return JsonResponse({"success": True})
        except User.DoesNotExist:
            return JsonResponse({"success": False, "error": "User not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})
def user_list(request):
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})
@login_required
def admin(request):
    return render(request, "users/admin.html")
def users_view(request):
    if request.method == 'POST':
            form = InterventionForm(request.POST)
            intervention = Intervention.objects.create(technicien=request.user, )
            if form.is_valid():
                intervention = form.save(commit=False)
                intervention.technicien = request.user  # Set the currently logged-in user
                intervention.save()
                intervention.Machine.status = "in_progress"
                intervention.Machine.save()
                # Update machine status
                if intervention.Machine and intervention.end_date:
                    intervention.Machine.status = "fixed"
                    intervention.Machine.save()
                return redirect('users:users')  # your success url
    else:
        form = InterventionForm()

    return render(request, 'users/users.html', {'form': form})
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
                return redirect("users:users")         
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})
def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect("users:login")   
#this function is used toadd new users
def users_list(request):
    if request.method == "POST":
            username = request.POST["ID"]
            first_name = request.POST["first_name"]           
            email = request.POST["email"]
            password = request.POST.get("password", "defaultpassword")
            role = request.POST["role"]

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists!")
            else:
                user = User.objects.create_user(username=username,first_name=first_name, email=email, password=password)

                # 🔥 Set role
                if role == "Admin":
                    user.is_staff = True
                    user.is_superuser = True
                else:  # role == "User"
                    user.is_staff = False
                    user.is_superuser = False

                user.save()
                messages.success(request, "User added successfully!")

            return redirect("users:users_list")

    users = User.objects.all()
    return render(request, 'users/users_list.html', {'users': users})