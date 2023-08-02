import django
from django.contrib.auth.models import User
from django.db import models
from main.models import Categories


class Estimated(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default='0')
    category_id = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(default=django.utils.timezone.now)

    def save(self, *args, **kwargs):
        if self.category_id.name != 'Przychody':
            if self.amount > 0:
                self.amount = self.amount * -1
        else:
            if self.amount < 0:
                self.amount = self.amount * -1
        super(Estimated, self).save(*args, **kwargs)
