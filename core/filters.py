import django_filters
from django.db.models import Q, QuerySet

from core import models


class DishFilter(django_filters.FilterSet):
    price = django_filters.RangeFilter(field_name='price', label='price of dish')
    comment = django_filters.CharFilter(field_name='comments__text', lookup_expr='icontains', label='Comment contains')
    term = django_filters.CharFilter(method='filter_term', label='all fields')

    class Meta:
        model = models.Dish
        fields = ['price', 'name', 'description']

    def filter_term(self, queryset: QuerySet, name: str, value: str) -> QuerySet:
        criterias = Q()
        for t in value.split():
            criterias &= Q(name__icontains=t) | Q(comments__text__icontains=t)
        return queryset.filter(criterias).distinct()
