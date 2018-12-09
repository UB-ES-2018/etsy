from django.db import models
from django.core.validators import MaxValueValidator

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    zipcode = models.IntegerField(verbose_name='zipcode',validators=[MaxValueValidator(99999)])
    city = models.CharField(verbose_name='city',max_length=50)
    country = models.CharField(verbose_name='country',max_length=50)
    street = models.CharField(verbose_name='street_name',max_length=50)



    def __str__(self):
        return f"{self.street}, {self.zipcode} {self.city} - {self.country}"