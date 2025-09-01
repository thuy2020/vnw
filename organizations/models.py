from django.db import models
from core.models import BaseEntity
from core.normalization import normalize_vietnamese_name


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
    normalized_name = models.CharField(max_length=255, editable=False, db_index=True)

    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = normalize_vietnamese_name(self.name)
        super().save(*args, **kwargs)
