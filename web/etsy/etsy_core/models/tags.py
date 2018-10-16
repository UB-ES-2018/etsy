from django.db import models

class Tags(models.Model):
    id = models.AutoField(primary_key=True)
    tags_name = models.CharField(
        verbose_name='tags_name',
        max_length=255,
        null=False)
    )

    def __str__(self):
        return 'Tag Name: %S' (self.tags_name)