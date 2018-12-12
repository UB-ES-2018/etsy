from django.db import models
from django.core.validators import MaxValueValidator

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    zipcode = models.CharField(verbose_name='zipcode',max_length=10,null=True,default=False)
    city = models.CharField(verbose_name='city',max_length=50,null=True,default=False)
    country = models.CharField(verbose_name='country',max_length=50,null=True,default=False)
    street = models.CharField(verbose_name='street_name',max_length=255,null=True,default=False)



    def __str__(self):
        return f"{self.street}, {self.zipcode} {self.city} - {self.country}"

    def is_valid(self):
        return self.zipcode != None and self.city != None and self.country != None and self.street != None