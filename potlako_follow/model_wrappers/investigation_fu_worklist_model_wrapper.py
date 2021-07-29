from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned
from edc_model_wrapper import ModelWrapper


class InvestigationWorkListModelWrapper(ModelWrapper):

    model = 'potlako_follow.investigationfuworklist'
    querystring_attrs = ['subject_identifier']
    next_url_attrs = ['subject_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'potlako_investigation_listboard_url')

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
    def cancer_propability_suspicion(self):
        baseline_clinical_cls = django_apps.get_model(
            'potlako_subject.baselineclinicalsummary')
        clinician_enrollment_cls = django_apps.get_model(
            'potlako_subject.cliniciancallenrollment')

        try:
            baseline_obj = baseline_clinical_cls.objects.get(
                                    subject_identifier=self.subject_identifier)
        except baseline_clinical_cls.DoesNotExist:
            try:
                clinician_enrollment_obj = clinician_enrollment_cls.objects.get(
                                                    subject_identifier=self.subject_identifier)
            except clinician_enrollment_cls.DoesNotExist:
                return None
            else:
                suspected_cancers = clinician_enrollment_obj.suspected_cancer
                if clinician_enrollment_obj.suspected_cancer_unsure:
                    suspected_cancers += ", " + clinician_enrollment_obj.suspected_cancer_unsure
                if clinician_enrollment_obj.suspected_cancer_other:
                    suspected_cancers += ", " + clinician_enrollment_obj.suspected_cancer_unsure

                return (suspected_cancers, clinician_enrollment_obj.suspicion_level)
        else:
            suspected_cancer = baseline_obj.cancer_concern or baseline_obj.cancer_concern_other
            return (suspected_cancer, baseline_obj.cancer_probability)

    @property
    def latest_investigation_ordered(self):
        investigation_ordered_cls = django_apps.get_model(
            'potlako_subject.investigationsordered')

        investigations_ordered = investigation_ordered_cls.objects.filter(
            subject_visit__subject_identifier=self.subject_identifier,
            tests_ordered_type__name='pathology')

        if investigations_ordered:
            return investigations_ordered.latest('created')

    @property
    def latest_investigation_resulted(self):
        investigation_resulted_cls = django_apps.get_model(
            'potlako_subject.investigationsresulted')

        investigations_resulted = investigation_resulted_cls.objects.filter(
            subject_visit__subject_identifier=self.subject_identifier,
            tests_resulted_type__name='pathology')

        if investigations_resulted:
            return investigations_resulted.latest('created')
