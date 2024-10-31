from rest_framework_json_api import serializers

from app import models


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = ['wallet', 'txid', 'amount']

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Wallet
        fields = ['label', 'balance', 'transactions']
        depth = 1
        read_only_fields = ['balance']
