from django.apps import apps as django_apps
from django.conf import settings

from potlako_dashboard.model_wrappers import (
    BaselineClinicalSummaryModelWrapperMixin, NavigationPlanSummaryModelWrapperMixin)
from edc_model_wrapper import ModelWrapper
from django.core.exceptions import MultipleObjectsReturned
from potlako_subject.models import SubjectScreening, SubjectConsent, ClinicianCallEnrollment


class NavigationWorkListModelWrapper(BaselineClinicalSummaryModelWrapperMixin,
                                     NavigationPlanSummaryModelWrapperMixin,
                                     ModelWrapper):

    model = 'potlako_follow.navigationworklist'
    querystring_attrs = ['subject_identifier']
    next_url_attrs = ['subject_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'potlako_navigation_listboard_url')

    @property
    def community_arm(self):
        onschedule_model_cls = django_apps.get_model(
            'potlako_subject.onschedule')
        try:
            onschedule_obj = onschedule_model_cls.objects.get(
                subject_identifier=self.subject_identifier)
        except ObjectDoesNotExist:
            return None
        else:
            return onschedule_obj.community_arm

    @property
    def gender(self):
        consent_model_cls = django_apps.get_model(
            'potlako_subject.subjectconsent')
        if self.subject_identifier:
            try:
                subject_consent_obj = consent_model_cls.object.get(
                    subject_identifier=self.subject_identifier)
            except subject_consent_obj.DoesNotExist:
                raise
            except MultipleObjectsReturned:
                return consent_model_cls.object.filter(
                    subject_identifier=self.subject_identifier)[0].gender
            else:
                return subject_consent_obj.gender
        return None

    @property
    def village_town(self):
        if self.subject_identifier:
            try:
                subject_consent_obj = SubjectConsent.objects.get(
                    subject_identifier=self.subject_identifier)
            except subject_consent_obj.DoesNotExist:
                raise
            else:
                screening_identifier = subject_consent_obj.screening_identifier
                clinical_call = ClinicianCallEnrollment.objects.get(screening_identifier=screening_identifier)
                return clinical_call.village_town.title()
