from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.filters import SearchFilter
from rest_framework_json_api import filters, django_filters

from app import models
from app.serializers import TransactionSerializer, WalletSerializer, ErrorResponseSerializer
from rest_framework import viewsets, status


@extend_schema(
    tags=['Transactions'],
    request=TransactionSerializer
)
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = models.Transaction.objects.all()
    serializer_class = TransactionSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # commented to reduce features testing complexity
    filter_backends = (filters.QueryParameterValidationFilter, filters.OrderingFilter,
                       django_filters.DjangoFilterBackend, SearchFilter)
    filterset_fields = {
        'txid': ('icontains', 'iexact', 'contains'),
        'amount': ('gte', 'lte', 'exact'),
    }
    search_fields = ('txid', 'amount',)

    @extend_schema(
        responses={
            status.HTTP_201_CREATED: TransactionSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(ErrorResponseSerializer, description="Not enough balance"),
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        responses={status.HTTP_200_OK: TransactionSerializer},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # allows only staff users to delete transactions
        # if not request.user.is_staff:
        #     return JsonResponse({'detail': 'Permission denied.'}, status=403)  # commented to reduce features testing complexity

        return super().destroy(request, *args, **kwargs)

    @extend_schema(exclude=True)
    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)

    @extend_schema(exclude=True)
    def partial_update(self, request, *args, **kwargs):
        super().partial_update(request, *args, **kwargs)


@extend_schema(
    tags=['Wallets'],
    request=WalletSerializer,
    )
class WalletViewSet(viewsets.ModelViewSet):
    queryset = models.Wallet.objects.all()
    serializer_class = WalletSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # commented to reduce features testing complexity
    filter_backends = (filters.QueryParameterValidationFilter, filters.OrderingFilter,
                       django_filters.DjangoFilterBackend, SearchFilter)
    filterset_fields = {
        'label': ('icontains', 'iexact', 'contains'),
        'balance': ('gte', 'lte', 'exact'),
    }
    search_fields = ('label', 'balance',)

    @extend_schema(
        responses={status.HTTP_201_CREATED: WalletSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        responses={status.HTTP_200_OK: WalletSerializer},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # allows only staff users to delete wallets
        # if not request.user.is_staff:
        #     return JsonResponse({'detail': 'Permission denied.'}, status=403)  # commented to reduce features testing complexity

        return super().destroy(request, *args, **kwargs)

    @extend_schema(exclude=True)
    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)

    @extend_schema(exclude=True)
    def partial_update(self, request, *args, **kwargs):
        super().partial_update(request, *args, **kwargs)
