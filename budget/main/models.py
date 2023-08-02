import django
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    balance = models.FloatField()
    # description = models.CharField(max_length=80)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Stan konta - wpis na kwotę {self.balance}.'


class Categories(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name

# models.SET_DEFAULT(set=), set null

class Expenses(models.Model):
    amount = models.DecimalField(max_digits=20, decimal_places=2, default='0')
    date = models.DateField(default=django.utils.timezone.now)
    description = models.CharField(max_length=80)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True, blank=True)


    def save(self, *args, **kwargs):
        if self.category_id.name != 'Przychody':
            if self.amount > 0:
                self.amount = self.amount * -1
        else:
            if self.amount < 0:
                self.amount = self.amount * -1
        super(Expenses, self).save(*args, **kwargs)

    def __str__(self):
        return f'Nowy wpis z kategorii {self.category_id.name} na kwotę {self.amount} z opisem {self.description}'
