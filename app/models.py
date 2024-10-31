from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.utils.translation.trans_real import translation


class Transaction(models.Model):
    wallet = models.ForeignKey('Wallet', on_delete=models.RESTRICT, related_name='transactions')
    txid = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=36, decimal_places=18)

    def save(self, *args, **kwargs):
        with transaction.atomic():

            super(Transaction, self).save(*args, **kwargs)
            new_balance = self.amount + self.wallet.balance
            if new_balance < 0:
                raise ValueError('Not enough balance')

            self.wallet.balance = new_balance
            self.wallet.save()



    def __str__(self):
        return self.txid

class Wallet(models.Model):
    label = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=36, decimal_places=18, validators=[MinValueValidator(0.0)], default=0)

    def __str__(self):
        return self.label
