from django.shortcuts import render
from .models import Intervention

# Create your views here.

def intervention_history(request):
    interventions = Intervention.objects.all().order_by('-received_date')  # Sort by most recent
    return render(request, 'maintenance/intervention_history.html', {'interventions': interventions})
