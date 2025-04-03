from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib import messages 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from maintenance.models import Intervention
from maintenance.forms import InterventionForm


@login_required
def edit_user(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        username = request.POST.get("username")
        email = request.POST.get("email")
        role = request.POST.get("role")

        try:
            user = User.objects.get(id=user_id)
            user.username = username
            user.email = email
            user.save()
            return JsonResponse({"success": True})
        except User.DoesNotExist:
            return JsonResponse({"success": False, "error": "User not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})

@login_required
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

# Create your views here.
@login_required
def admin(request):
    return render(request, "users/admin.html")

def users_view(request):
    user = request.user
    interventions = Intervention.objects.all().order_by("-received_date")
    if request.method == "POST":
        # Extract data from request.POST
        received_date = request.POST.get("received_date")
        end_date = request.POST.get("end_date")
        fault_category = request.POST.get("fault_category")
        fault_what = request.POST.getlist("fault_what")  # Handling multiple selections
        comments = request.POST.get("comments")

        # Create and save the intervention
        intervention = Intervention.objects.create(
            technicien=request.user,  # Assign the logged-in user
            received_date=received_date,
            end_date=end_date,
            fault_category=fault_category,
            fault_what=fault_what,
            comments=comments,
        )
        intervention.save()
        logout(request)
        print(request.POST.getlist('fault_what'))
        return redirect('users:login')
    return render(request,"users/users.html")

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
    
def users_list(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST.get("password", "defaultpassword")  # Ensure a password is set
        role = request.POST["role"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "User added successfully!")

        return redirect("users:users_list")  

    users = User.objects.all()
    return render(request, 'users/users_list.html', {'users': users})