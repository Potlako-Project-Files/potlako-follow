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

    high = ListboardFilter(
        label='High',
        position=12,
        lookup={'cancer_probability': 'high'})

    moderate = ListboardFilter(
        label='Moderate',
        position=12,
        lookup={'cancer_probability': 'Moderate'})

    low = ListboardFilter(
        label='Low',
        position=12,
        lookup={'cancer_probability': 'Low'})
