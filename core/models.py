from django.db import models

class BaseEntity(models.Model):
    custom_id = models.CharField(max_length=20, unique=True, blank=True)

    class Meta:
        abstract = True

    def generate_custom_id(self, prefix):
        ModelClass = self.__class__
        last = (
            ModelClass.objects.filter(custom_id__startswith=prefix)
            .order_by("-custom_id")
            .first()
        )
        if last and last.custom_id[len(prefix):].isdigit():
            next_id = int(last.custom_id[len(prefix):]) + 1
        else:
            next_id = 1
        return f"{prefix}{next_id:05d}"

    def save(self, *args, **kwargs):
        if not self.custom_id:
            prefix = getattr(self, 'CUSTOM_ID_PREFIX', 'ENT')
            self.custom_id = self.generate_custom_id(prefix)
        super().save(*args, **kwargs)