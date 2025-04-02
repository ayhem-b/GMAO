from django.urls import path
from .views import intervention_history,intervention_data,machines_charts
app_name = 'maintenance'
urlpatterns = [
    path('intervention-history/', intervention_history, name='intervention_history'),
    path('intervention-data/', intervention_data, name='intervention_data'),
    path('machines_charts/', machines_charts, name='machines_charts'),
]


