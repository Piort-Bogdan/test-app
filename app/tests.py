from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User

from app import models


class TestTransaction(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='test', password='test')

        self.test_wallet = models.Wallet.objects.create(label='test')
        self.test_transaction = models.Transaction.objects.create(wallet=self.wallet, txid='test', amount=10)

    def test_create_wallet(self):
        client = APIClient()
        client.login(username='test', password='test')

        response = client.post('/api/v1/wallets/', {'label': 'new_wallet'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Wallet.objects.count(), 2)
        self.assertEqual(models.Wallet.objects.get(id=response.data['id']).label, 'new_wallet')

    def test_balance_gets_negative(self):
        client = APIClient()
        client.login(username='test', password='test')

        response = client.post('/api/v1/transactions/', {'wallet': self.test_wallet.id, 'txid': 'tx2', 'amount': -20},
                               format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Not enough balance', response.data['non_field_errors'])

    def test_balance_increment_by_transaction(self):
        client = APIClient()
        client.login(username='test', password='test')

        response = client.post('/api/v1/transactions/', {'wallet': self.test_wallet.id, 'txid': 'tx2', 'amount': 20},
                               format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.test_wallet.refresh_from_db()
        self.assertEqual(self.test_wallet.balance, 30)

    def test_delete_wallet(self):
        client = APIClient()
        client.login(username='test', password='test')

        response = client.delete(f'/api/v1/wallets/{self.test_wallet.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(models.Wallet.objects.count(), 0)

    def test_create_transaction(self):
        client = APIClient()
        client.login(username='test', password='test')

        response = client.post('/api/v1/transactions/', {'wallet': self.test_wallet.id, 'txid': 'tx2', 'amount': 20},
                               format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Transaction.objects.count(), 2)
        self.assertEqual(models.Transaction.objects.get(txid='tx2').amount, 20)

    def test_delete_transaction(self):
        client = APIClient()
        client.login(username='test', password='test')

        response = client.delete(f'/api/v1/transactions/{self.test_transaction.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(models.Transaction.objects.count(), 0)
