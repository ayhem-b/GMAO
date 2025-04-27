from django import forms
from .models import Intervention ,WorkOrder, Machine

class InterventionForm(forms.ModelForm):
    class Meta:
        model = Intervention
        fields = [
            "technicien",
            "Machine",
            "received_date",
            "end_date",
            "fault_category",
            "fault_what",
            "fault_why",
            "fault_where",
            "used_spare_parts",
            "comments",
        ]
        widgets = {
            "received_date": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "end_date": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "fault_category": forms.Select(attrs={"class": "form-control"}),
            "fault_what": forms.Select(attrs={"class": "form-control"}),
            "fault_why": forms.Select(attrs={"class": "form-control"}),
            "fault_where": forms.Select(attrs={"class": "form-control"}),
            "spare_parts": forms.Select(attrs={"class": "form-control"}),
            "technicien": forms.Select(attrs={"class": "form-control"}),
            "Machine": forms.Select(attrs={"class": "form-control"}),
            "comments": forms.Textarea(attrs={"class": "form-control"}),
        }
class WorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = ['machine_id', 'time_of_default', 'description', 'assigned_user']
        widgets = {
            'time_of_default': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ['name', 'machine_id', 'description', 'status']
        widgets = {
            'status': forms.Select(choices=Machine.STATUS_CHOICES),
        }