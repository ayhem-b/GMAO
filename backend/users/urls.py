from django.urls import path
from . import views
from .views import edit_user, delete_user
app_name = 'users'
urlpatterns = [
   path('register/',views.register,name='register'),
   path('',views.user_login,name='login'),
   path('logout/',views.user_logout,name='logout'),
   path('admin/',views.admin,name='admin'),
   path('users/',views.users_view,name='users'),
   path('users_list/', views.users_list, name='users_list'),
   path('edit-user/', edit_user, name='edit-user'),
   path('delete-user/', delete_user, name='delete-user'),
]