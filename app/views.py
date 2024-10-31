from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework.authtoken.models import Token
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework_json_api import filters, django_filters

from app import models
from app.serializers import TransactionSerializer, WalletSerializer
from rest_framework import viewsets, permissions, status

@extend_schema(
    tags=['Auth'],
    responses={200: {'token': 'string'}},
)
class CustomAuthToken(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return JsonResponse({
            'token': token.key,
        }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['Transactions'],
    request=TransactionSerializer,
    responses={201: TransactionSerializer},
    methods=['GET', 'POST', 'DELETE'],
    )
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = models.Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.QueryParameterValidationFilter, filters.OrderingFilter,
                       django_filters.DjangoFilterBackend, SearchFilter)
    filterset_fields = {
        'txid': ('icontains', 'iexact', 'contains'),
        'amount': ('gte', 'lte', 'exact'),
    }
    search_fields = ('txid', 'amount',)

    def destroy(self, request, *args, **kwargs):
        # allows only staff users to delete transactions
        if not request.user.is_staff:
            return JsonResponse({'detail': 'Permission denied.'}, status=403)

        return super().destroy(request, *args, **kwargs)


@extend_schema(
    tags=['Wallets'],
    request=TransactionSerializer,
    responses={201: TransactionSerializer},
    methods=['GET', 'POST', 'DELETE'],
    )
class WalletViewSet(viewsets.ModelViewSet):
    queryset = models.Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.QueryParameterValidationFilter, filters.OrderingFilter,
                       django_filters.DjangoFilterBackend, SearchFilter)
    filterset_fields = {
        'label': ('icontains', 'iexact', 'contains'),
        'balance': ('gte', 'lte', 'exact'),
    }
    search_fields = ('label', 'balance',)

    def destroy(self, request, *args, **kwargs):
        # allows only staff users to delete wallets
        if not request.user.is_staff:
            return JsonResponse({'detail': 'Permission denied.'}, status=403)

        return super().destroy(request, *args, **kwargs)
