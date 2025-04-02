from django.shortcuts import render
from .models import Intervention
from django.http import JsonResponse
from collections import Counter
from datetime import datetime
from django.db.models.functions import TruncDate
from django.db.models import Count
from django.db.models import Sum, F, ExpressionWrapper, DurationField
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

    # ⚙️ Count by Fault What
    fault_what_data = {}
    for intervention in interventions:
        for fault in intervention.fault_what:
            fault_what_data[fault] = fault_what_data.get(fault, 0) + 1
    fault_what_data = {
        "labels": list(fault_what_data.keys()),
        "values": list(fault_what_data.values())
    }

    # 🔧 Count by Fault Why
    fault_why_data = {}
    for intervention in interventions:
        for reason in intervention.fault_why:
            fault_why_data[reason] = fault_why_data.get(reason, 0) + 1
    fault_why_data = {
        "labels": list(fault_why_data.keys()),
        "values": list(fault_why_data.values())
    }

    # 🏭 Count by Fault Where
    fault_where_data = {}
    for intervention in interventions:
        for location in intervention.fault_where:
            fault_where_data[location] = fault_where_data.get(location, 0) + 1
    fault_where_data = {
        "labels": list(fault_where_data.keys()),
        "values": list(fault_where_data.values())
    }

    # 🛠️ Spare Parts Usage
    spare_parts_data = {}
    for intervention in interventions:
        for part in intervention.spare_parts:
            spare_parts_data[part] = spare_parts_data.get(part, 0) + 1
    spare_parts_data = {
        "labels": list(spare_parts_data.keys()),
        "values": list(spare_parts_data.values())
    }

    # 📅 Interventions Over Time
    timeline_data = interventions.extra({"day": "date(received_date)"}).values("day").annotate(count=Count("id")).order_by("day")
    timeline_data = {
        "labels": [str(entry["day"]) for entry in timeline_data],
        "values": [entry["count"] for entry in timeline_data]
    }

  # ✅ Fix: Calculate total downtime in hours
    downtime_data = (
        Intervention.objects.filter(end_date__isnull=False)
        .annotate(
            downtime=ExpressionWrapper(
                F('end_date') - F('received_date'), output_field=DurationField()
            )
        )
        .aggregate(total_downtime=Sum('downtime'))
    )

    # Convert downtime to hours (PostgreSQL stores duration in seconds)
    total_downtime_hours = downtime_data['total_downtime'].total_seconds() / 3600 if downtime_data['total_downtime'] else 0

def intervention_data(request):
    # ✅ Fix: Calculate total downtime in hours
    downtime_data = (
        Intervention.objects.filter(end_date__isnull=False)
        .annotate(
            downtime=ExpressionWrapper(
                F('end_date') - F('received_date'), output_field=DurationField()
            )
        )
        .aggregate(total_downtime=Sum('downtime'))
    )

    # Convert downtime to hours
    total_downtime_hours = downtime_data['total_downtime'].total_seconds() / 3600 if downtime_data['total_downtime'] else 0

    # Example of other statistics (replace with actual queries)
    category_data = {"labels": ["MNP", "MCP", "AUT"], "values": [10, 5, 3]}
    fault_what_data = {"labels": ["Mécanique", "Électrique"], "values": [7, 8]}
    fault_why_data = {"labels": ["Usure", "Blocage"], "values": [4, 6]}
    fault_where_data = {"labels": ["Sewing", "Line UP"], "values": [5, 7]}
    spare_parts_data = {"labels": ["Pièce A", "Pièce B"], "values": [3, 2]}
    timeline_data = {"labels": ["2025-04-01", "2025-04-02"], "values": [6, 4]}

    # ✅ Merge all data into a single JSON response
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