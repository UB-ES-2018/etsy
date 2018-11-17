from django.db import models


class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(
        verbose_name='category_name',
        max_length=255,
        null=False)
    is_default = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return f"Option Name: {self.category_name}"

    def get_fields(self):
        for field in self.optionfield_set.all():
            yield field