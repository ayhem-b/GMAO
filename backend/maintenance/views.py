from django.shortcuts import render,redirect, get_object_or_404
from .models import Intervention, Machine
from django.http import JsonResponse
from collections import Counter
from datetime import datetime
from django.db.models import Count, Sum, F, ExpressionWrapper, DurationField
from django.db.models.functions import TruncDate
from maintenance.forms import WorkOrderForm , MachineForm,InterventionForm
from django.contrib.auth.decorators import login_required
from .models import WorkOrder
from maintenance.models import Intervention, Machine
import json
from django.views.decorators.csrf import csrf_exempt
from plc_manager_instance import plc

last_inputs = {}
PLC_IP = '192.168.10.5'
# Create your views here.
def intervention_history(request):
    interventions = Intervention.objects.all().order_by('-received_date')  # Sort by most recent
    return render(request, 'maintenance/intervention_history.html', {'interventions': interventions})
def intervention_data(request):
    interventions = Intervention.objects.all()
    

    # 📊 Count by Fault Category
    category_counts = interventions.values("fault_category").annotate(count=Count("fault_category"))
    category_data = {
        "labels": [c["fault_category"] for c in category_counts],
        "values": [c["count"] for c in category_counts]
    }

    # ⚙️ Count by Fault What, Why, Where, Spare Parts
    fault_what_data, fault_why_data, fault_where_data, spare_parts_data = {}, {}, {}, {}

    for intervention in interventions:
        # Ensure fault_what is not None before splitting it
        if intervention.fault_what:
            for fault in intervention.fault_what if isinstance(intervention.fault_what, list) else intervention.fault_what.split(","):
                fault_what_data[fault.strip()] = fault_what_data.get(fault.strip(), 0) + 1

        if intervention.fault_why:
            for reason in intervention.fault_why if isinstance(intervention.fault_why, list) else intervention.fault_why.split(","):
                fault_why_data[reason.strip()] = fault_why_data.get(reason.strip(), 0) + 1

        if intervention.fault_where:
            for location in intervention.fault_where if isinstance(intervention.fault_where, list) else intervention.fault_where.split(","):
                fault_where_data[location.strip()] = fault_where_data.get(location.strip(), 0) + 1

        if intervention.spare_parts:
            for part in intervention.spare_parts if isinstance(intervention.spare_parts, list) else intervention.spare_parts.split(","):
                spare_parts_data[part.strip()] = spare_parts_data.get(part.strip(), 0) + 1

    # Convert data to lists
    fault_what_data = {"labels": list(fault_what_data.keys()), "values": list(fault_what_data.values())}
    fault_why_data = {"labels": list(fault_why_data.keys()), "values": list(fault_why_data.values())}
    fault_where_data = {"labels": list(fault_where_data.keys()), "values": list(fault_where_data.values())}
    spare_parts_data = {"labels": list(spare_parts_data.keys()), "values": list(spare_parts_data.values())}

    # 📅 Interventions Over Time
    timeline_counts = interventions.annotate(date=TruncDate("received_date")).values("date").annotate(count=Count("id")).order_by("date")
    timeline_data = {
        "labels": [str(entry["date"]) for entry in timeline_counts],
        "values": [entry["count"] for entry in timeline_counts]
    }
   
    # ⏳ Total Downtime in Hours
    downtime_data = (
        interventions.filter(end_date__isnull=False)
        .annotate(downtime=ExpressionWrapper(F("end_date") - F("received_date"), output_field=DurationField()))
        .aggregate(total_downtime=Sum("downtime"))
    )

    total_downtime_hours = downtime_data["total_downtime"].total_seconds() / 3600 if downtime_data["total_downtime"] else 0
    user_counts = (
        interventions.values("technicien__first_name")
        .annotate(count=Count("id"))
        .order_by("technicien__first_name")
    )
    user_data = {
        "labels": [entry["technicien__first_name"] for entry in user_counts],
        "values": [entry["count"] for entry in user_counts]
    }
    # ✅ Return JSON Response
    
    return JsonResponse({
        "categories": category_data,
        "faults_what": fault_what_data,
        "faults_why": fault_why_data,
        "faults_where": fault_where_data,
        "spare_parts": spare_parts_data,
        "timeline": timeline_data,
        "downtime": {
            "labels": ["Total Downtime"],
            "values": [total_downtime_hours]
        },
        "users": user_data
    })
def machines_charts(request):
    if request.method == 'POST':
        form = MachineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('maintenance:machines_charts')
    else:
        form = MachineForm()
        machine=Machine.objects.all()
    return render(request, "maintenance/machines_charts.html", {'machine': machine, 'form': form})
def work_order(request):
    if request.method == 'POST':
        form = WorkOrderForm(request.POST)
        if form.is_valid():
            work_order = form.save()  # Save the form and get the work order instance
            work_order.status="waiting"
            work_order.save()
            #update the machine status
            work_order.machine_id.status = "not_fixed"  # machine_id is the ForeignKey to Machine
            work_order.machine_id.save()  # Save the updated machine status

            return redirect('maintenance:work_order')  # Redirect after saving
    else:
        form = WorkOrderForm()

    work_orders = WorkOrder.objects.all().order_by("-created_at") # Get all work orders
    return render(request, 'maintenance/work_order.html', {'form': form, 'work_orders': work_orders})
def breakdowns(request):

    # Fetch all work orders from the database
    work_orders = WorkOrder.objects.all()
    return render(request, 'maintenance/breakdowns.html', {'work_orders': work_orders})
def user_work_order(request):
    orders = WorkOrder.objects.all().order_by('-created_at')
    return render(request, 'maintenance/user_work_orders.html', {'orders': orders})
def add_intervention(request):
    work_order_id = request.GET.get('work_order_id')
    work_order = get_object_or_404(WorkOrder, pk=work_order_id)

    if request.method == 'POST':
        form = InterventionForm(request.POST)
        if form.is_valid():
            intervention = form.save(commit=False)
            intervention.technicien = request.user
            intervention.work_order = work_order
            intervention.work_order.status="in_progress"
            intervention.work_order.save()
            intervention.Machine.status = "in_progress"
            intervention.Machine.save()
            intervention.save()

            # Update machine status if needed
            if intervention.Machine and intervention.end_date:
                intervention.Machine.status = "fixed"
                intervention.work_order.status="fixed"
                intervention.work_order.save()
                intervention.Machine.save()

            return redirect('users:users')  # Redirect after success
    else:
        form = InterventionForm(initial={'work_order': work_order})

    return render(request, 'users/users.html', {
        'form': form,
        'work_order': work_order,
    })
@csrf_exempt
@csrf_exempt
def update_inputs(request):
    global last_inputs
    if request.method == "POST":
        data = json.loads(request.body)
        last_inputs.update(data)
        return JsonResponse({'status': 'updated'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def get_inputs(request):
    return JsonResponse(plc.get_inputs())

@csrf_exempt
def write_memory_bit(request):
    if request.method == "POST":
        data = json.loads(request.body)
        bit = int(data.get('bit', 0))
        value = bool(data.get('value', 0))
        plc.queue_write(bit, value)
        return JsonResponse({"status": "queued", "bit": bit, "value": value})
    return JsonResponse({"error": "Invalid request"}, status=400)

def dashboard(request):
    input_bits = [f"I{byte}.{bit}" for byte in range(2) for bit in range(8)]  # I0.0 to I1.7
    return render(request, 'maintenance/dashboard.html', {'input_bits': input_bits})

