from django.urls import path
from .views import intervention_history,intervention_data,machines_charts,work_order,breakdowns
app_name = 'maintenance'
urlpatterns = [
    path('intervention-history/', intervention_history, name='intervention_history'),
    path('intervention-data/', intervention_data, name='intervention_data'),
    path('machines_charts/', machines_charts, name='machines_charts'),
    path('work_order/', work_order, name='work_order'),
    path('breakdowns/', breakdowns, name='breakdowns'),
]


