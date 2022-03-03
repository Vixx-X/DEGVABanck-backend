from django_filters import rest_framework as filters
from degvabank.apps.transaction.models import Transaction


class TransaccionFilter(filters.FilterSet):
    min_amount = filters.NumberFilter(field_name="amount", lookup_expr='gte')
    max_amount = filters.NumberFilter(field_name="amount", lookup_expr='lte')
    amount = filters.NumberFilter(field_name="amount", lookup_expr='exact')

    source = filters.CharFilter(field_name="source", lookup_expr='icontains')
    target = filters.CharFilter(field_name="target", lookup_expr='icontains')

    min_date = filters.DateFilter(field_name="date", lookup_expr="gte")
    max_date = filters.DateFilter(field_name="date", lookup_expr="lte")

    type = filters.CharFilter(field_name="type", lookup_expr="exact")
    status = filters.CharFilter(field_name="status", lookup_expr="exact")

    reason = filters.CharFilter(field_name="reason", lookup_expr="icontains")

    id = filters.NumberFilter(field_name="id", lookup_expr="exact")

    class Meta:
        model = Transaction
        fields = [
            "min_amount",
            "max_amount",
            "amount",
            "source",
            "target",
            "min_date",
            "max_date",
            "type",
            "status",
            "reason",
            "id",
        ]
