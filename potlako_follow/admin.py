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

from .admin_site import potlako_follow_admin
from .forms import LogEntryForm, NavigationWorkListForm, WorkListForm
from .models import Call, Log, LogEntry, WorkList, NavigationWorkList


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


@admin.register(Call, site=potlako_follow_admin)
class CallAdmin(ModelAdminMixin, ModelAdminCallMixin, admin.ModelAdmin):
    pass


@admin.register(Log, site=potlako_follow_admin)
class LogAdmin(ModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(LogEntry, site=potlako_follow_admin)
class LogEntryAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = LogEntryForm

    search_fields = ['study_maternal_identifier']

    date_hierarchy = 'appt_date'

    fieldsets = (
        (None, {
            'fields': (
                'log',
                'call_reason',
                'call_datetime',
                'contact_type',
                'time_of_week',
                'time_of_day',
                'appt',
                'appt_reason_unwilling',
                'appt_reason_unwilling_other',
                'appt_date',
                'appt_grading',
                'appt_location',
                'appt_location_other',
                'may_call',
            )},
         ),
        audit_fieldset_tuple
    )

    radio_fields = {
        'call_reason': admin.VERTICAL,
        'contact_type': admin.VERTICAL,
        'time_of_week': admin.VERTICAL,
        'time_of_day': admin.VERTICAL,
        'appt': admin.VERTICAL,
        'appt_reason_unwilling': admin.VERTICAL,
        'appt_grading': admin.VERTICAL,
        'appt_location': admin.VERTICAL,
        'may_call': admin.VERTICAL,
    }

    list_display = (
        'log',
        'call_datetime',
        'appt',
        'appt_date',
        'may_call',
    )

    list_filter = (
        'call_datetime',
        'appt',
        'appt_date',
        'may_call',
        'created',
        'modified',
        'hostname_created',
        'hostname_modified',
    )

    search_fields = ('id', 'log__call__subject_identifier')


@admin.register(WorkList, site=potlako_follow_admin)
class WorkListAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = WorkListForm

    fieldsets = (
        (None, {
            'fields': (
                'subject_identifier',
                'study_maternal_identifier',
                'report_datetime',
                'prev_study',
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
                'study_maternal_identifier',
                'report_datetime',
                'prev_study',
                'is_called',
                'called_datetime',
                'visited',)}),
        audit_fieldset_tuple)

    instructions = ['Complete this form once per day.']