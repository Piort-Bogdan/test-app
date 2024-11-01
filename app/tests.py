from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User

from app import models


class TestTransaction(TestCase):
    def setUp(self):
        # self.test_user = User.objects.create_user(username='test', password='test')

        self.test_wallet = models.Wallet.objects.create(label='test')

    def test_create_wallet(self):
        client = APIClient()

        response = client.post('/api/v1/wallets/', {
              "data": {
                "type": "Wallet",
                "attributes": {
                  "label": "test_label"
                }
              }
            })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Wallet.objects.count(), 2)
        self.assertEqual(models.Wallet.objects.get(id=response.data['id']).label, 'test_label')

    def test_balance_gets_negative(self):
        client = APIClient()
        # client.login(username='test', password='test')

        response = client.post('/api/v1/transactions/', {
            "data": {
                "type": "Transaction",
                "attributes": {
                  "txid": "test_txid",
                  "amount": "-10"
                },
                "relationships": {
                  "wallet": {
                    "data": {
                      "id": self.test_wallet.id,
                      "type": "Wallet"
                    }
                  }
            }
            }
        })

        self.test_wallet.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0]['detail'], 'Not enough balance')

    def test_balance_increment_by_transaction(self):
        client = APIClient()
        # client.login(username='test', password='test')

        response = client.post('/api/v1/transactions/', {
            "data": {
                "type": "Transaction",
                "attributes": {
                    "txid": "test_txid",
                    "amount": "400"
                },
                "relationships": {
                    "wallet": {
                        "data": {
                            "id": self.test_wallet.id,
                            "type": "Wallet"
                        }
                    }
                }
            }
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.test_wallet.refresh_from_db()
        self.assertEqual(self.test_wallet.balance, 400)

    def test_delete_wallet(self):
        client = APIClient()
        # client.login(username='test', password='test')

        response = client.delete(f'/api/v1/wallets/{self.test_wallet.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(models.Wallet.objects.count(), 0)

    def test_delete_transaction(self):
        client = APIClient()
        # client.login(username='test', password='test')

        self.test_transaction = models.Transaction.objects.create(wallet=self.test_wallet, txid='test_txid', amount=400)
        response = client.delete(f'/api/v1/transactions/{self.test_transaction.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(models.Transaction.objects.count(), 0)
