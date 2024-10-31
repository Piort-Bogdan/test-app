from django.core.validators import MinValueValidator
from django.db import models


class Transaction(models.Model):
    wallet = models.ForeignKey('Wallet', on_delete=models.RESTRICT, related_name='transactions')
    txid = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=36, decimal_places=18)

    def __str__(self):
        return self.txid

    class Meta:
        ordering = ['id']


class Wallet(models.Model):
    label = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=36, decimal_places=18, validators=[MinValueValidator(0.0)], default=0)

    def __str__(self):
        return self.label

    class Meta:
        ordering = ['id']
