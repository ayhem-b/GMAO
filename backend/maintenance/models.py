from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Intervention(models.Model):
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

    # Fault Codes (Multiple Choices)
    FAULT_WHAT_CHOICES = [
        ('Mécanique', 'Mécanique'),
        ('Électrique', 'Électrique'),
        ('Pneumatique', 'Pneumatique'),
        ('Hydraulique', 'Hydraulique'),
        ('Maintenance', 'Maintenance'),
        ('Logiciel', 'Logiciel'),
        ('Inspection', 'Inspection'),
    ]
    fault_what = models.JSONField(default=list,null=True, blank=True)  # Store multiple selections

    FAULT_WHY_CHOICES = [
        ('Cassure', 'Cassure'),
        ('Usure', 'Usure'),
        ('Saleté', 'Saleté'),
        ('Blocage', 'Blocage'),
        ('Desserrage', 'Desserrage'),
        ('Surcharge', 'Surcharge'),
        ('Mauvaise utilisation', 'Mauvaise utilisation'),
        ('Mauvais réglage', 'Mauvais réglage'),
        ('Alimentation électrique', 'Alimentation électrique'),
        ('Court-circuit', 'Court-circuit'),
    ]
    fault_why = models.JSONField(default=list,null=True, blank=True)

    FAULT_WHERE_CHOICES = [
        ('Sewing', 'Sewing'),
        ('Line UP', 'Line UP'),
        ('Punch', 'Punch'),
        ('Fawl', 'Fawl'),
        ('PC', 'PC'),
        ('Amada', 'Amada'),
        ('Ondule', 'Ondule'),
        ('Imprimante', 'Imprimante'),
        ('Lecteur Code à Barre', 'Lecteur Code à Barre'),
        ('Lampe éclairage', 'Lampe éclairage'),
        ('Caméra', 'Caméra'),
        ('Presse sertissage', 'Presse sertissage'),
        ('Armoire électrique', 'Armoire électrique'),
        ('Bloc électrovanne', 'Bloc électrovanne'),
        ('Système de guidage', 'Système de guidage'),
        ('Tête Sewing', 'Tête Sewing'),
    ]
    fault_where = models.JSONField(default=list,null=True, blank=True)

    # Spare Parts
    spare_parts = models.JSONField(default=list,null=True, blank=True)  # Store part reference and quantity

    # Technician Comments
    comments = models.TextField(blank=True,null=True)

    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Intervention by {self.technicien.username} on {self.received_date}"