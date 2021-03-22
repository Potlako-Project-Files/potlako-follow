import re

from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls.base import reverse
from django.utils.decorators import method_decorator
from edc_base.utils import get_utcnow

from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import (
    ListboardFilterViewMixin, SearchFormViewMixin)
from edc_dashboard.views import ListboardView
from edc_navbar import NavbarViewMixin

from ..model_wrappers import WorkListModelWrapper
from ..models import WorkList
from .filters import ListboardViewFilters
from .worklist_queryset_view_mixin import WorkListQuerysetViewMixin


class ListboardView(NavbarViewMixin, EdcBaseViewMixin,
                    ListboardFilterViewMixin, SearchFormViewMixin,
                    WorkListQuerysetViewMixin,
                    ListboardView):

    listboard_template = 'potlako_follow_listboard_template'
    listboard_url = 'potlako_follow_listboard_url'
    listboard_panel_style = 'info'
    listboard_fa_icon = "fa-user-plus"

    model = 'potlako_follow.worklist'
    listboard_view_filters = ListboardViewFilters()
    model_wrapper_cls = WorkListModelWrapper
    navbar_name = 'potlako_follow'
    navbar_selected_item = 'appointmet_worklist'
    ordering = '-modified'
    paginate_by = 10
    search_form_url = 'potlako_follow_listboard_url'

    def specilist_appointment_date(self, subject_identifier=None):
        patient_initial_cls = django_apps.get_model('potlako_subject.patientcallinitial')
        patient_fu_cls = django_apps.get_model('potlako_subject.patientcallfollowup')

        patient_fu_obj = patient_fu_cls.objects.filter(
            subject_visit__subject_identifier=subject_identifier).order_by('-created')
        if patient_fu_obj:
            return patient_fu_obj[0].next_appointment_date
        else:
            try:
                patient_call_obj = patient_initial_cls.objects.get(
                    subject_visit__subject_identifier=subject_identifier)
            except patient_initial_cls.DoesNotExist:
                pass
            else:
                return patient_call_obj.next_appointment_date
        return None

    @property
    def create_worklist(self):
        subject_consent_cls = django_apps.get_model('potlako_subject.subjectconsent')
        subject_identifiers = subject_consent_cls.objects.values_list(
            'subject_identifier', flat=True).all()
        subject_identifiers = list(set(subject_identifiers))
        for subject_identifier in subject_identifiers:
            if self.specilist_appointment_date(subject_identifier=subject_identifier):
                if self.specilist_appointment_date(
                        subject_identifier=subject_identifier) <= get_utcnow().date():
                    try:
                        WorkList.objects.get(subject_identifier=subject_identifier)
                    except WorkList.DoesNotExist:
                        WorkList.objects.create(
                            subject_identifier=subject_identifier)
                else:
                    WorkList.objects.filter(
                            subject_identifier=subject_identifier).delete()

    def get_success_url(self):
        return reverse('potlako_follow:potlako_follow_listboard_url')

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
            total_results=self.get_queryset().count(),
            called_subject=WorkList.objects.filter(is_called=True).count(),
            visited_subjects=WorkList.objects.filter(visited=True).count())
        return context
