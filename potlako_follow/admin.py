from django.contrib import admin
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_base.sites.admin import ModelAdminSiteMixin
from edc_model_admin import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin,
    ModelAdminReadOnlyMixin, ModelAdminInstitutionMixin,
    ModelAdminRedirectOnDeleteMixin)
from edc_model_admin import audit_fieldset_tuple
from edc_call_manager.admin import ModelAdminCallMixin
from potlako_subject.models.model_mixins import BaselineRoadMapMixin

from .admin_site import potlako_follow_admin
from .forms import LogEntryForm, NavigationWorkListForm, WorkListForm, InvestigationFUWorkListForm
from .models import Call, Log, LogEntry, WorkList, NavigationWorkList, InvestigationFUWorkList


class ModelAdminMixin(ModelAdminNextUrlRedirectMixin,
                      ModelAdminFormInstructionsMixin,
                      ModelAdminFormAutoNumberMixin, ModelAdminRevisionMixin,
                      ModelAdminAuditFieldsMixin, ModelAdminReadOnlyMixin,
                      ModelAdminInstitutionMixin,
                      ModelAdminRedirectOnDeleteMixin,
                      ModelAdminSiteMixin):

    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'

    def add_view(self, request, form_url='', extra_context=None):

        extra_context = extra_context or {}
        if self.extra_context_models:
            extra_context_dict = BaselineRoadMapMixin(
                subject_identifier=request.GET.get(
                    'subject_identifier')).baseline_dict
            [extra_context.update({key: extra_context_dict.get(key)})for key in self.extra_context_models]
        return super().add_view(
            request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):

        extra_context = extra_context or {}
        if self.extra_context_models:
            extra_context_dict = BaselineRoadMapMixin(
                subject_identifier=request.GET.get(
                    'subject_identifier')).baseline_dict
            [extra_context.update({key: extra_context_dict.get(key)})for key in self.extra_context_models]
        return super().change_view(
            request, object_id, form_url=form_url, extra_context=extra_context)


@admin.register(Call, site=potlako_follow_admin)
class CallAdmin(ModelAdminMixin, ModelAdminCallMixin, admin.ModelAdmin):
    pass


@admin.register(Log, site=potlako_follow_admin)
class LogAdmin(ModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(LogEntry, site=potlako_follow_admin)
class LogEntryAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = LogEntryForm
    instructions = None

    extra_context_models = [
        'cliniciancallenrollment',
        'navigationsummaryandplan', ]

    search_fields = ['subject_identifier']

    fieldsets = (
        (None, {
            'fields': ('log',
                       'subject_identifier',
                       'call_datetime',
                       'patient_reached',
                       'call_outcome',)
        }), audit_fieldset_tuple)

    radio_fields = {'patient_reached': admin.VERTICAL,
                    'call_outcome': admin.VERTICAL}

    list_display = (
        'subject_identifier', 'call_datetime',)

    def get_all_fields(self, instance):
        """"
        Return names of all available fields from given Form instance.

        :arg instance: Form instance
        :returns list of field names
        :rtype: list
        """

        fields = list(instance.base_fields)

        for field in list(instance.declared_fields):
            if field not in fields:
                fields.append(field)
        return fields

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['log'].queryset = \
            Log.objects.filter(id=request.GET.get('log'))
        return super(LogEntryAdmin, self).render_change_form(
            request, context, *args, **kwargs)


@admin.register(WorkList, site=potlako_follow_admin)
class WorkListAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = WorkListForm

    fieldsets = (
        (None, {
            'fields': (
                'subject_identifier',
                'report_datetime',
                'is_called',
                'called_datetime',
                'visited',)}),
        audit_fieldset_tuple)

    instructions = ['Complete this form once per day.']


@admin.register(NavigationWorkList, site=potlako_follow_admin)
class NavigationWorkListAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = NavigationWorkListForm

    fieldsets = (
        (None, {
            'fields': (
                'subject_identifier',
                'report_datetime',
                'is_called',
                'called_datetime',
                'visited',)}),
        audit_fieldset_tuple)

    instructions = ['Complete this form once per day.']


@admin.register(InvestigationFUWorkList, site=potlako_follow_admin)
class InvestigationFUWorkListAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = InvestigationFUWorkListForm

    fieldsets = (
        (None, {
            'fields': (
                'subject_identifier',
                'report_datetime',
                'is_called',
                'called_datetime',
                'visited',)}),
        audit_fieldset_tuple)

    instructions = ['Complete this form once per day.']
