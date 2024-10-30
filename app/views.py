import models
from serializers import TransactionSerializer, WalletSerializer
from rest_framework import viewsets


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = models.Transaction.objects.all()
    serializer_class = TransactionSerializer


class WalletViewSet(viewsets.ModelViewSet):
    queryset = models.Wallet.objects.all()
    serializer_class = WalletSerializer
