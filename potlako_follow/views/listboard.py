import re
from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls.base import reverse
from django.utils.decorators import method_decorator
from edc_base.utils import get_utcnow
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin

from edc_dashboard.view_mixins import (
    ListboardFilterViewMixin, SearchFormViewMixin)
from edc_dashboard.views import ListboardView

from ..model_wrappers import WorkListModelWrapper
from ..models import WorkList
from .filters import ListboardViewFilters
from .worklist_queryset_view_mixin import WorkListQuerysetViewMixin


class ListboardView(EdcBaseViewMixin, NavbarViewMixin,
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
    navbar_selected_item = 'appointment_worklist'
    ordering = '-cancer_probability_rank'
    paginate_by = 50
    search_form_url = 'potlako_follow_listboard_url'

    @property
    def create_worklist(self):
        subject_consent_cls = django_apps.get_model(
            'potlako_subject.subjectconsent')

        appt_cls = django_apps.get_model('edc_appointment.appointment')

        overdue_appts_obj = appt_cls.objects.filter(appt_datetime__lte=get_utcnow().date(),
                                                    appt_status='new')

        overdue_appts_ids = overdue_appts_obj.values_list(
            'subject_identifier', flat=True).distinct()

        old_worklist = WorkList.objects.all().exclude(
            subject_identifier__in=overdue_appts_ids)
        old_worklist.delete()

        for appt in overdue_appts_obj:

            latest_consent = subject_consent_cls.objects.filter(
                subject_identifier=appt.subject_identifier).last()

            if latest_consent:
                try:
                    WorkList.objects.filter(
                        subject_identifier=appt.subject_identifier).last()
                except WorkList.DoesNotExist:
                    WorkList.objects.create(
                        subject_identifier=appt.subject_identifier,
                        user_created=latest_consent.user_created)

    def get_community_arm(self, subject_identifier):
        onschedule_model_cls = django_apps.get_model(
            'potlako_subject.onschedule')
        try:
            onschedule_obj = onschedule_model_cls.objects.filter(
                subject_identifier=subject_identifier).last()
        except onschedule_model_cls.DoesNotExist:
            return None
        else:
            return onschedule_obj.community_arm

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
        if re.match('^[a-z]+$', search_term):
            q = Q(user_created__icontains=search_term) | Q(
                cancer_probability=search_term)
        return q

    def get_queryset(self):
        return super().get_queryset().order_by(
            '-specialist_appointment_date').order_by('-cancer_probability_rank')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.create_worklist
        context.update(
            total_results=self.get_queryset().count(),
            called_subject=WorkList.objects.filter(is_called=True).count(),
            visited_subjects=WorkList.objects.filter(visited=True).count())
        return context
