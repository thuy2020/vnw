from django.db import models
from people.models import Person
from organizations.models import Organization

class Legislation(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    law_number = models.CharField(max_length=100, blank=True, null=True)
    date_passed = models.DateField(blank=True, null=True)
    date_effective = models.DateField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)

    people_involved = models.ManyToManyField(Person, through='PersonLegislation')
    organizations_involved = models.ManyToManyField(Organization, through='OrganizationLegislation')

    def __str__(self):
        return self.title


class PersonLegislation(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    legislation = models.ForeignKey(Legislation, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, blank=True, null=True)  # e.g., Sponsor, Supporter, Opponent

    def __str__(self):
        return f"{self.person.name} — {self.role or 'Involved'} in {self.legislation.title}"

class OrganizationLegislation(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    legislation = models.ForeignKey(Legislation, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, blank=True, null=True)  # e.g., Advocate, Opposed, Neutral

    def __str__(self):
        return f"{self.organization.name} — {self.role or 'Involved'} in {self.legislation.title}"