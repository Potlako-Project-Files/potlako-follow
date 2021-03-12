from django.apps import apps as django_apps
from django.contrib import admin
from django.conf import settings
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch

from edc_model_admin.model_admin_next_url_redirect_mixin import ModelAdminNextUrlRedirectError
from edc_constants.constants import NOT_APPLICABLE
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
                       'phone_num_type',
                       'phone_num_success',)
        }),

        ('Subject Cell & Telephones', {
            'fields': ('cell_contact_fail',
                       'alt_cell_contact_fail',
                       'tel_contact_fail',
                       'alt_tel_contact_fail',)
        }),
        ('Subject Work Contact', {
            'fields': ('work_contact_fail',)
        }),
        ('Indirect Contact Cell & Telephone', {
            'fields': ('cell_alt_contact_fail',
                       'tel_alt_contact_fail',)
        }),
        ('Schedule Appointment With Participant', {
           'fields': ('appt',
                      'appt_reason_unwilling',
                      'appt_reason_unwilling_other',
                      'appt_date',
                      'appt_grading',
                      'appt_location',
                      'appt_location_other',
                      'may_call',
                      'home_visit',
                      'home_visit_other',)
        }), audit_fieldset_tuple)

    radio_fields = {'appt': admin.VERTICAL,
                    'appt_reason_unwilling': admin.VERTICAL,
                    'appt_grading': admin.VERTICAL,
                    'appt_location': admin.VERTICAL,
                    'may_call': admin.VERTICAL,
                    'cell_contact_fail': admin.VERTICAL,
                    'alt_cell_contact_fail': admin.VERTICAL,
                    'tel_contact_fail': admin.VERTICAL,
                    'alt_tel_contact_fail': admin.VERTICAL,
                    'work_contact_fail': admin.VERTICAL,
                    'cell_alt_contact_fail': admin.VERTICAL,
                    'tel_alt_contact_fail': admin.VERTICAL,
                    'cell_resp_person_fail': admin.VERTICAL,
                    'tel_resp_person_fail': admin.VERTICAL,
                    'home_visit': admin.VERTICAL}

    list_display = (
        'subject_identifier', 'call_datetime', )

    def get_form(self, request, obj=None, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)

        if obj:
            subject_identifier = getattr(obj, 'subject_identifier', '')
        else:
            subject_identifier = request.GET.get('subject_identifier')

        fields = self.get_all_fields(form)

        for idx, field in enumerate(fields):
            custom_value = self.custom_field_label(subject_identifier, field)

            if custom_value:
                form.base_fields[field].label = f'{idx +1}. Why was the contact to {custom_value} unsuccessful?'
        form.custom_choices = self.phone_choices(subject_identifier)
        return form

    def redirect_url(self, request, obj, post_url_continue=None):
        redirect_url = super().redirect_url(
            request, obj, post_url_continue=post_url_continue)
        if ('none_of_the_above' not in obj.phone_num_success
                and obj.home_visit == NOT_APPLICABLE):
            if request.GET.dict().get('next'):
                url_name = settings.DASHBOARD_URL_NAMES.get(
                    'subject_listboard_url')
            options = {'subject_identifier': request.GET.dict().get('subject_identifier')}
            try:
                redirect_url = reverse(url_name, kwargs=options)
            except NoReverseMatch as e:
                raise ModelAdminNextUrlRedirectError(
                    f'{e}. Got url_name={url_name}, kwargs={options}.')
        return redirect_url

    def phone_choices(self, study_identifier):
        subject_locator_cls = django_apps.get_model(
            'potlako_subject.subjectlocator')
        field_attrs = [
            'subject_cell',
            'subject_cell_alt',
            'subject_phone',
            'subject_phone_alt',
            'subject_work_phone',
            'indirect_contact_cell',
            'indirect_contact_phone', ]

        try:
            locator_obj = subject_locator_cls.objects.get(
                subject_identifier=study_identifier)
        except subject_locator_cls.DoesNotExist:
            pass
        else:
            phone_choices = ()
            for field_attr in field_attrs:
                value = getattr(locator_obj, field_attr)
                if value:
                    field_name = field_attr.replace('_', ' ')
                    value = f'{value} {field_name.title()}'
                    phone_choices += ((field_attr, value),)
            return phone_choices

    def custom_field_label(self, study_identifier, field):
        subject_locator_cls = django_apps.get_model(
            'potlako_subject.subjectlocator')
        fields_dict = {
            'cell_contact_fail': 'subject_cell',
            'alt_cell_contact_fail': 'subject_cell_alt',
            'tel_contact_fail': 'subject_phone',
            'alt_tel_contact_fail': 'subject_phone_alt',
            'work_contact_fail': 'subject_work_phone',
            'cell_alt_contact_fail': 'indirect_contact_cell',
            'tel_alt_contact_fail': 'indirect_contact_phone'}

        try:
            locator_obj = subject_locator_cls.objects.get(
                subject_identifier=study_identifier)
        except subject_locator_cls.DoesNotExist:
            pass
        else:
            attr_name = fields_dict.get(field, None)
            if attr_name:
                return getattr(locator_obj, attr_name, '')

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
