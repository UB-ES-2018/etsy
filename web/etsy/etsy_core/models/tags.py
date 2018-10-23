from django.db import models


class Tags(models.Model):
    id = models.AutoField(primary_key=True)
    tags_name = models.CharField(
        verbose_name='tag_name',
        max_length=255,
        null=False)

    def __str__(self):
        return f"Tag Name: {self.get__name()}"

    # Our own properties
    def get__name(self):
        # The product is identified by its name
        return self.tags_name
