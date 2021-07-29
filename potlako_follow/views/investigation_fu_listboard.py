import re

from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls.base import reverse
from django.utils.decorators import method_decorator

from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import (
    ListboardFilterViewMixin, SearchFormViewMixin)
from edc_dashboard.views import ListboardView
from edc_navbar import NavbarViewMixin

from potlako_subject.models import InvestigationsOrdered, InvestigationsResulted

from ..model_wrappers import InvestigationWorkListModelWrapper
from ..models import InvestigationFUWorkList
from .filters import ListboardViewFilters
from .worklist_queryset_view_mixin import WorkListQuerysetViewMixin
from edc_constants.constants import YES


class InvestigationFUListboardView(NavbarViewMixin, EdcBaseViewMixin,
                                   ListboardFilterViewMixin, SearchFormViewMixin,
                                   WorkListQuerysetViewMixin,
                                   ListboardView):

    listboard_template = 'potlako_investigation_listboard_template'
    listboard_url = 'potlako_investigation_listboard_url'
    listboard_panel_style = 'info'
    listboard_fa_icon = "fa-user-plus"

    model = 'potlako_follow.investigationfuworkList'
    listboard_view_filters = ListboardViewFilters()
    model_wrapper_cls = InvestigationWorkListModelWrapper
    navbar_name = 'potlako_follow'
    navbar_selected_item = 'investigation_fu_worklist'
    ordering = '-modified'
    paginate_by = 10
    search_form_url = 'potlako_investigation_listboard_url'

    @property
    def create_worklist(self):
        investigation_ordered_cls = django_apps.get_model(
            'potlako_subject.investigationsordered')
        investigation_resulted_cls = django_apps.get_model(
            'potlako_subject.investigationsresulted')

        resulted_subject_identifiers = investigation_resulted_cls.objects.values_list(
            'subject_visit__subject_identifier', flat=True).filter(
                tests_resulted_type__name='pathology',
                results_reviewed=YES)

        ordered_subject_identifiers = investigation_ordered_cls.objects.values_list(
            'subject_visit__subject_identifier', flat=True).filter(
                tests_ordered_type__name='pathology').exclude(
                    subject_visit__subject_identifier__in=resulted_subject_identifiers)

        ordered_subject_identifiers = list(set(ordered_subject_identifiers))

        for subject_identifier in ordered_subject_identifiers:

            subject_investigations_ordered = InvestigationsOrdered.objects.filter(
                tests_ordered_type__name='pathology',
                subject_visit__subject_identifier=subject_identifier)

            if (subject_investigations_ordered
                    and self.get_community_arm(subject_identifier) == 'Intervention'):
                try:
                    InvestigationsResulted.objects.get(
                        tests_resulted_type__name='pathology',
                        subject_visit__subject_identifier=subject_identifier,
                        results_reviewed=YES)
                except InvestigationsResulted.DoesNotExist:
                    try:
                        InvestigationFUWorkList.objects.get(
                            subject_identifier=subject_identifier)
                    except InvestigationFUWorkList.DoesNotExist:
                        InvestigationFUWorkList.objects.create(
                            subject_identifier=subject_identifier)
                else:
                    InvestigationFUWorkList.objects.filter(
                            subject_identifier=subject_identifier).delete()
            else:
                InvestigationFUWorkList.objects.filter(
                                subject_identifier=subject_identifier).delete()

        InvestigationFUWorkList.objects.filter(
            subject_identifier__in=resulted_subject_identifiers).delete()

    def get_success_url(self):
        return reverse('potlako_follow:potlako_investigation_listboard_url')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        if kwargs.get('subject_identifier'):
            options.update(
                {'subject_identifier': kwargs.get('subject_identifier')})
        return options

    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Z]+$', search_term):
            q = Q(first_name__exact=search_term)
        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.create_worklist
        context.update(
        )
        return context

    def get_community_arm(self, subject_identifier):
        onschedule_model_cls = django_apps.get_model(
            'potlako_subject.onschedule')
        try:
            onschedule_obj = onschedule_model_cls.objects.get(
                subject_identifier=subject_identifier)
        except onschedule_model_cls.DoesNotExist:
            return None
        else:
            return onschedule_obj.community_arm
