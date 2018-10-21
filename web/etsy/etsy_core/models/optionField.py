from django.db import models
from .options import Options


class OptionField(models.Model):
    id = models.AutoField(primary_key=True)
    options_id = models.ForeignKey(Options, on_delete=models.CASCADE)
    field_name = models.CharField(
        verbose_name='field_name',
        max_length=255,
        null=False)

    def __str__(self):
        return f"Field Name: {self.field_name} of Option: {self.options_id.options_name}"
