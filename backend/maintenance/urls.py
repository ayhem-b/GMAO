from django.urls import path
from .views import intervention_history,intervention_data,machines_charts,work_order,breakdowns,user_work_order,add_intervention,update_inputs,get_inputs,dashboard,write_memory_bit
app_name = 'maintenance'
urlpatterns = [
    path('intervention-history/', intervention_history, name='intervention_history'),
    path('intervention-data/', intervention_data, name='intervention_data'),
    path('machines_charts/', machines_charts, name='machines_charts'),
    path('work_order/', work_order, name='work_order'),
    path('breakdowns/', breakdowns, name='breakdowns'),
    path('user_work-orders',user_work_order, name='user_work_order'),
    path('add_intervention/', add_intervention, name='add_intervention'),
    path('update-inputs/', update_inputs),
    path('update-inputs/', update_inputs),
    path('get-inputs/', get_inputs),
    path('dashboard/', dashboard,name='dashboard'),
   path('write-memory-bit/', write_memory_bit),

]


