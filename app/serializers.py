from django.db import transaction
from django.db.models import Sum
from rest_framework_json_api import serializers

from app import models


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = ['wallet', 'txid', 'amount']

    def create(self, validated_data):
        with transaction.atomic():
            transaction_instance = super().create(validated_data)

            new_balance = transaction_instance.wallet.transactions.aggregate(amount_total=Sum('amount'))[
                              'amount_total'] or 0

            # check for sufficient balance
            if new_balance < 0:
                raise serializers.ValidationError("Not enough balance")

            # Update wallet balance
            transaction_instance.wallet.balance = new_balance
            transaction_instance.wallet.save(update_fields=['balance'])

            return transaction_instance


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Wallet
        fields = ['label', 'balance', 'transactions']
        depth = 1
        read_only_fields = ['balance']
