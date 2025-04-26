from django.shortcuts import render,redirect
from .models import Intervention
from django.http import JsonResponse
from collections import Counter
from datetime import datetime
from django.db.models import Count, Sum, F, ExpressionWrapper, DurationField
from django.db.models.functions import TruncDate
from maintenance.forms import WorkOrderForm
from django.contrib.auth.decorators import login_required
from .models import WorkOrder
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
        # Ensure correct type (handles JSONField or string storage)
        for fault in intervention.fault_what if isinstance(intervention.fault_what, list) else intervention.fault_what.split(","):
            fault_what_data[fault.strip()] = fault_what_data.get(fault.strip(), 0) + 1

        for reason in intervention.fault_why if isinstance(intervention.fault_why, list) else intervention.fault_why.split(","):
            fault_why_data[reason.strip()] = fault_why_data.get(reason.strip(), 0) + 1

        for location in intervention.fault_where if isinstance(intervention.fault_where, list) else intervention.fault_where.split(","):
            fault_where_data[location.strip()] = fault_where_data.get(location.strip(), 0) + 1

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
        }
    })
def machines_charts(request):
    return render(request, "maintenance/machines_charts.html")


def create_work_order(request):
    if request.method == 'POST':
        form = WorkOrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('maintenance:machines_charts')  # Redirect to a page listing work orders
    else:
        form = WorkOrderForm()
        orders = WorkOrder.objects.all()
    return render(request, 'maintenance/create_work_order.html', {'form': form,'orders': orders})




@login_required
def work_order_list(request):

    return render(request, 'maintenance/work_orders_list.html')