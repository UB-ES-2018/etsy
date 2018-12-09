from django.db import models
#from django.core.validators import MaxValueValidator

class Address(models.Model):
    zipcode = models.IntegerField(verbose_name='zipcode',required=True)
    city = models.CharField(verbose_name='city',max_length=50,required=True)
    country = models.CharField(verbose_name='country',max_length=50, required=True)
    street = models.charField(verbose_name='street_name',max_length=50, required=True)



    def __str__(self):
        return f"{self.street}, {self.zipcode} {self.city} - {self.country}"