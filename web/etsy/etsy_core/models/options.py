from django.db import models


class Options(models.Model):
    id = models.AutoField(primary_key=True)
    options_name = models.CharField(
        verbose_name='options_name',
        max_length=255,
        null=False)
    is_default = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return f"Option Name: {self.options_name}"
