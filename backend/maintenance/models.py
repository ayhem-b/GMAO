from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField



User = get_user_model()
# Machine model
class Machine(models.Model):
    STATUS_CHOICES = [
        ('default', 'Default Issued'),
        ('in_progress', 'In Progress'),
        ('fixed', 'Fixed Now'),
        ('not_fixed', 'Not Fixed'),
    ]
    name = models.CharField(max_length=255)
    machine_id = models.IntegerField(unique=True)  # Unique identifier for the machine
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='default')


    def __str__(self):
        return f"{self.name} ({self.machine_id}) - {self.description}"
    
#workorder model
class WorkOrder(models.Model):
 

    machine_name = models.CharField(max_length=255)
    machine_id =models.ForeignKey('Machine', on_delete=models.CASCADE)  # ForeignKey to Machine model
    time_of_default = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_user = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.machine_name} - {self.status}"
    


# spare parts model
class SparePart(models.Model):
    part_name = models.CharField(max_length=255)
    part_number = models.CharField(max_length=255, unique=True)  # Unique identifier for the part
    quantity = models.IntegerField(default=0)  # Quantity in stock
    def __str__(self):
        return f"{self.part_name} ({self.part_number}) - {self.quantity} in stock"
    

# intervention model

class Intervention(models.Model):
    work_order = models.ForeignKey(WorkOrder,null=True, blank=True, on_delete=models.CASCADE)
    technicien = models.ForeignKey(User, on_delete=models.CASCADE)  # Assigned Technician
    received_date = models.DateTimeField(null=True,blank=True)  # Date Received
    end_date = models.DateTimeField(null=True, blank=True)  # Completion Date
    
    # Fault Category
    CATEGORY_CHOICES = [
        ('MNP', 'Maintenance Non Planifiée'),
        ('MCP', 'Maintenance Curative Planifiée'),
        ('AUT', 'Travaux Divers ou Amélioration'),
    ]
    fault_category = models.CharField(max_length=3, choices=CATEGORY_CHOICES,null=True, blank=True)

    Machine=models.ForeignKey(Machine, on_delete=models.CASCADE, null=True, blank=True)  # ForeignKey to Machine model
    fault_what = models.JSONField(default=list,null=True, blank=True)  # Store multiple selections

    fault_why = models.JSONField(default=list,null=True, blank=True)


    fault_where = models.JSONField(default=list,null=True, blank=True)

    # Spare Parts
    spare_parts = models.JSONField(default=list,null=True, blank=True)  # Store part reference and quantity

    # Technician Comments
    comments = models.TextField(blank=True,null=True)

    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Intervention by {self.technicien.username} on {self.received_date}"


