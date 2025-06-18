from django.db import models

class OrganizationUnit(models.Model):
    name = models.CharField(max_length=225)
    type = models.CharField(max_length=225, choices=[
        ('department_level1', 'Department Level 1'),
        ('department_level2', 'Department Level 2'),
        ('department_level3', 'Department Level 3'),
        ('department_level4', 'Department Level 4'),
        ('department_level5', 'Department Level 5'),

    ])

    parent = models.ForeignKey('self', related_name='children',
                               on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# Create your models here.
