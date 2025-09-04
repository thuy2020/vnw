from django.db import models
from core.models import BaseEntity
from core.normalization import normalize_vietnamese_name
# --- Admin Safeguard for Manual Entry ---
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver

from unidecode import unidecode

class OrganizationRelationship(models.Model):
    from_org = models.ForeignKey('Organization', related_name='related_parent_links', on_delete=models.CASCADE)
    to_org = models.ForeignKey('Organization', related_name='related_child_links', on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('from_org', 'to_org')

    def __str__(self):
        return f"{self.to_org} → {self.from_org} ({self.notes})"

class OrganizationType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
class Organization(BaseEntity):
    CUSTOM_ID_PREFIX = "ORG"
    name = models.CharField(max_length=225)
    name_en = models.CharField(max_length=225, blank=True, null=True)

    abbreviation = models.CharField(max_length=50, blank=True, null=True)

    type = models.ForeignKey(
        'OrganizationType',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    level = models.CharField(
        max_length=50,
        choices=[
            ('central', 'Central'),
            ('provincial', 'Provincial'),
            ('district', 'District'),
            ('commune', 'Commune')
        ],
        blank=True,
        null=True
    )

    function = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    color_code = models.CharField(max_length=20, blank=True, null=True)

    parent = models.ForeignKey('self', related_name='children',
                               on_delete=models.CASCADE, null=True, blank=True)

    equivalents = models.ManyToManyField('self', symmetrical=True, blank=True)
    related_parents = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        related_name='related_children',
        through='OrganizationRelationship',
        through_fields=('to_org', 'from_org')
    )


    description = models.TextField(blank=True, null=True)
    normalized_name = models.CharField(max_length=255, editable=False, db_index=True, unique=True, null=True, blank=True)
    name_ascii = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    def __str__(self):
        return self.name

    def clean(self):
        # Normalize the name to detect duplicates
        normalized = unidecode(' '.join((self.name or '').split())).lower()
        existing = Organization.objects.filter(normalized_name=normalized)

        if self.pk:
            existing = existing.exclude(pk=self.pk)

        if existing.exists():
            raise ValidationError(f"❌ Organization with name '{self.name}' already exists.")

    def save(self, *args, **kwargs):
        if self.name:
            self.normalized_name = unidecode(' '.join(self.name.split())).lower()
        self.full_clean()  # <--- ensures clean() is called even from admin
        super().save(*args, **kwargs)