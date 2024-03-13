import django_filters
from . models import *

class BookFilter(django_filters.FilterSet):
    # quantity = django_filters.NumberFilter()
    title = django_filters.CharFilter(field_name='title')
    class Meta:
        model = Books
        fields = ['title']