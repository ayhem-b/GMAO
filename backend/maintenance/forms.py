from django import forms
from .models import Intervention

class InterventionForm(forms.ModelForm):
    class Meta:
        model = Intervention
        fields = [
            "received_date",
            "end_date",
            "fault_category",
            "fault_what",
            "fault_why",
            "fault_where",
            "spare_parts",
            "comments",
        ]
        widgets = {
            "received_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "fault_what": forms.CheckboxSelectMultiple(),
            "fault_why": forms.CheckboxSelectMultiple(),
            "fault_where": forms.CheckboxSelectMultiple(),
        }
