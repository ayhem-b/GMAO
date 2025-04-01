from django.urls import path
from .views import intervention_history
app_name = 'maintenance'
urlpatterns = [
    path('intervention-history/', intervention_history, name='intervention_history'),
]