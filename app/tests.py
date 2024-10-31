from django.test import TestCase

from app import models


class TestTransaction(TestCase):
    def setUp(self):

        self.wallet = models.Wallet.objects.create(label='test')
        self.transaction = models.Transaction.objects.create(wallet=self.wallet, txid='test', amount=10)

    def test_not_enough_balance(self):
        pass
