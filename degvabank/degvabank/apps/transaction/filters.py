from django_filters import rest_framework as filters
from degvabank.apps.transaction.models import Transaction

class TransaccionFilter(filters.FilterSet):
    min_amount = filters.NumberFilter(field_name="amount", lookup_expr='gte')
    max_amount = filters.NumberFilter(field_name="amount", lookup_expr='lte')

    source = filters.CharFilter(field_name="source", lookup_expr='contains')
    target = filters.CharFilter(field_name="target", lookup_expr='contains')

    min_date = filters.DateFilter(field_name="date", lookup_expr='gte')
    max_date = filters.DateFilter(field_name="date", lookup_expr='lte')

    type = filters.CharFilter(field_name="type", lookup_expr="exact")
    status = filters.CharFilter(field_name="status", lookup_expr="exact")

    reason = filters.CharFilter(field_name="reason", lookup_expr="contains")

    class Meta:
        model = Transaction
        fields = ['min_amount', 'max_amount', 'source', 'target', 
                  'min_date', 'max_date', 'type', 'status', 'reason']