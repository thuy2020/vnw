from django.db import models
from core.models import BaseEntity


class OrganizationUnit(BaseEntity):
    CUSTOM_ID_PREFIX = "ORG"
    name = models.CharField(max_length=225)

    ORG_TYPE_CHOICES = [
        ('ministry', 'Ministry'),
        ('department', 'Department'),
        ('company', 'Company'),
        # Add more as needed
    ]

    type = models.CharField(max_length=100, choices=ORG_TYPE_CHOICES)

    parent = models.ForeignKey('self', related_name='children',
                               on_delete=models.CASCADE, null=True, blank=True)

    equivalents = models.ManyToManyField('self', symmetrical=True, blank=True)

    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
