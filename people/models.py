from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=100)
    year_of_birth = models.IntegerField(null=True, blank=True)
    hometown = models.CharField(max_length=100, null=True, blank=True)
    current_workplace = models.CharField(max_length=100, null=True, blank=True)
    current_workposition = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.name
