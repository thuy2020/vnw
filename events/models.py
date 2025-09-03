from django.db import models
from people.models import Person
from organizations.models import Organization
from legislation.models import Legislation

class Event(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)  # e.g., protest, speech, meeting

    people_involved = models.ManyToManyField(Person, through='PersonEvent')
    organizations_involved = models.ManyToManyField(Organization, through='OrganizationEvent')
    legislations_involved = models.ManyToManyField(Legislation, blank=True)

    def __str__(self):
        return self.title


class PersonEvent(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, blank=True, null=True)  # e.g., speaker, participant, organizer

    def __str__(self):
        return f"{self.person.name} ({self.role or 'Involved'}) in '{self.event.title}'"


class OrganizationEvent(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, blank=True, null=True)  # e.g., sponsor, opponent

    def __str__(self):
        return f"{self.organization.name} ({self.role or 'Involved'}) in '{self.event.title}'"