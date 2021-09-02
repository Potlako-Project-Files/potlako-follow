from edc_dashboard.listboard_filter import ListboardFilter, ListboardViewFilters
from django.apps import apps as django_apps


class ListboardViewFilters(ListboardViewFilters):

    all = ListboardFilter(
        name='all',
        label='All',
        lookup={})

    is_called = ListboardFilter(
        label='Called',
        position=10,
        lookup={'is_called': True})

    visited = ListboardFilter(
        label='Visited',
        position=11,
        lookup={'visited': True})
