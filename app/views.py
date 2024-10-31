from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter
from rest_framework_json_api import filters, django_filters

from app import models
from app.serializers import TransactionSerializer, WalletSerializer
from rest_framework import viewsets

@extend_schema(
    tags=['Transactions'],
    request=TransactionSerializer,
    responses={201: TransactionSerializer},
    )
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = models.Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = (filters.QueryParameterValidationFilter, filters.OrderingFilter,
                       django_filters.DjangoFilterBackend, SearchFilter)
    filterset_fields = {
        'txid': ('icontains', 'iexact', 'contains'),
        'amount': ('gte', 'lte', 'exact'),
    }
    search_fields = ('txid', 'amount',)


@extend_schema(
    tags=['Wallets'],
    request=TransactionSerializer,
    responses={201: TransactionSerializer},
    )
class WalletViewSet(viewsets.ModelViewSet):
    queryset = models.Wallet.objects.all()
    serializer_class = WalletSerializer
    filter_backends = (filters.QueryParameterValidationFilter, filters.OrderingFilter,
                       django_filters.DjangoFilterBackend, SearchFilter)
    filterset_fields = {
        'label': ('icontains', 'iexact', 'contains'),
        'balance': ('gte', 'lte', 'exact'),
    }
    search_fields = ('label', 'balance',)
