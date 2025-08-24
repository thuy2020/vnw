from django.db import models
from core.models import BaseEntity

class Cabinet(models.Model):
    name = models.CharField(max_length=300)
    url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Person(BaseEntity):
    CUSTOM_ID_PREFIX = "IND"
    name = models.CharField(max_length=200)
    hometown = models.CharField(max_length=200, blank=True, null=True)
    date_of_birth = models.CharField(max_length=20, blank=True, null=True)
    resume_text = models.TextField(null=True, blank=True)

    #optional fields
    resume_url = models.URLField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)

    date_of_death = models.CharField(max_length=20, blank=True, null=True)
    ethnicity = models.CharField(max_length=100, blank=True, null=True)

    date_entered_party = models.CharField(max_length=20, blank=True, null=True)
    date_entered_party_official = models.CharField(max_length=20, blank=True, null=True)
    expertise = models.CharField(max_length=200, blank=True, null=True)
    education = models.CharField(max_length=200, blank=True, null=True)
    political_theory = models.CharField(max_length=100, blank=True, null=True)
    foreign_language = models.CharField(max_length=200, blank=True, null=True)
    position = models.CharField(max_length=200, blank=True, null=True)
    degree = models.CharField(max_length=100, blank=True, null=True)
    rank = models.CharField(max_length=100, blank=True, null=True)
    position_process = models.TextField(blank=True, null=True)


    # Many-to-Many to cabinets
    cabinets = models.ManyToManyField(Cabinet, related_name="members", blank=True)

    #ensure unique combination of these
    class Meta:
        unique_together = ("name", "hometown", "date_of_birth")


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.custom_id:
            self.custom_id = self.generate_custom_id("IND")
        super().save(*args, **kwargs)

class PersonPosition(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='positions')
    title = models.CharField(max_length=1000)
    start = models.CharField(max_length=20, blank=True, null=True)
    end = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.person.name} — {self.title} ({self.start or '...'} to {self.end or '...'} )"
