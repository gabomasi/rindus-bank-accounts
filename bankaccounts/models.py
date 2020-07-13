from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models as GisModels


class User(AbstractUser):
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, related_name='users_created', null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     self.full_clean()
    #     return super(User, self).save(*args, **kwargs)
    #
    # def clean(self):
    #     raise ValidationError('You can not edit this user, it was not created by you')
    #     super(User, self).clean()


class BankAccount(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='bank_accounts')
    iban = models.CharField(max_length=100)

    def __str__(self):
        return self.iban


class AreaEfector(models.Model):
    nombre = GisModels.CharField(max_length=35)
    hospital = GisModels.CharField(max_length=150)
    fuente = GisModels.CharField(max_length=100)
    observ = GisModels.CharField(max_length=254)
    cobertura = GisModels.CharField(max_length=50)
    geom = GisModels.MultiPolygonField(srid=4326)
