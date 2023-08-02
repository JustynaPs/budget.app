import django_filters
from django import forms
from django.db.models import Q
from django.http import request
from django_filters import ModelChoiceFilter

from .models import Expenses

import django_filters
from .models import Expenses, Categories


# class ExpensesFilterForm(forms.Form):
#     start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
#     end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

# class CategoryChoiceFilter(ModelChoiceFilter):
#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         queryset = Categories.objects.filter(
#             Q(user_id=user) | Q(is_default=True, user_id=None)
#         )
#         super().__init__(*args, queryset=queryset, **kwargs)


class ExpensesFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name="date", lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name="date", lookup_expr='lte')
    # category_id = CategoryChoiceFilter(field_name="category_id", user=...)
    category_id = django_filters.ModelChoiceFilter(queryset=Categories.objects.all())
    amount_from = django_filters.NumberFilter(field_name="amount", lookup_expr='gte')
    amount_to = django_filters.NumberFilter(field_name="amount", lookup_expr='lte')

    def filter_start_date(self, queryset, name, value):
        if value:
            queryset = queryset.filter(date__gte=value)
        return queryset

    def filter_end_date(self, queryset, name, value):
        if value:
            queryset = queryset.filter(date__lte=value)
        return queryset

    class Meta:
        model = Expenses
        fields = ['start_date', 'end_date', 'category_id', 'amount_from', 'amount_to']