from django.urls import path
from .views import intervention_history,intervention_data,machines_charts,create_work_order,work_order_list
app_name = 'maintenance'
urlpatterns = [
    path('intervention-history/', intervention_history, name='intervention_history'),
    path('intervention-data/', intervention_data, name='intervention_data'),
    path('machines_charts/', machines_charts, name='machines_charts'),
     path('create-work-order/', create_work_order, name='create_work_order'),
    path('work-orders/', work_order_list, name='work_order_list'),
]


