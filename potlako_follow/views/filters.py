from cgitb import lookup
import imp
from turtle import pos
from edc_dashboard.listboard_filter import ListboardFilter, ListboardViewFilters
from django.apps import apps as django_apps
from potlako_subject.models import ClinicianCallEnrollment

class ListboardViewFilters(ListboardViewFilters):
    
    
    current_user = ListboardFilter(
        label='My Worklist',
        position=1,
        
        lookup={'user_created': ''})
    

    all = ListboardFilter(
        name='all',
        label='All',
        position=2,
        lookup={})

    is_called = ListboardFilter(
        label='Called',
        position=3,
        lookup={'is_called': True})

    visited = ListboardFilter(
        label='Visited',
        position=4,
        lookup={'visited': True})

    high = ListboardFilter(
        label='High',
        position=5,
        lookup={'cancer_probability': 'high'})

    moderate = ListboardFilter(
        label='Moderate',
        position=6,
        lookup={'cancer_probability': 'Moderate'})

    low = ListboardFilter(
        label='Low',
        position=7,
        lookup={'cancer_probability': 'Low'})


class NavigationListboardViewFilters(ListboardViewFilters):
    pass

