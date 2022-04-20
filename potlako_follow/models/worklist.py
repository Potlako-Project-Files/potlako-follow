
from django.db import models
from django.db.models import *
from edc_search.model_mixins import SearchSlugManager
from urllib3 import Retry
from .worklist_model_mixin import WorkListModelMixin, BaseWorkManager
from django.apps import apps as django_apps
from queryable_properties.properties import queryable_property
from queryable_properties.managers import QueryablePropertiesManager
from potlako_subject.models import BaselineClinicalSummary
from django.db.models import Subquery, QuerySet, OuterRef, Count
from edc_base.utils import get_utcnow


class WorklistManager(BaseWorkManager, SearchSlugManager):

    baseline_clinical_summary_model = 'potlako_subject.baselineclinicalsummary'
    log_entry_model = 'potlako_follow.logentry'

    @property
    def log_entry_cls(self):
        return django_apps.get_model(self.log_entry_model)

    @property
    def baseline_clinical_summary_cls(self):
        return django_apps.get_model(self.baseline_clinical_summary_model)

    @property
    def appointment_cls(self):
        return django_apps.get_model('edc_appointment.appointment')

    def get_queryset(self):
        """
        Overriding the queryset in order to include a calculated value
        so one can use filter on a calcuated property or attribute
        """

        base_clinical_summary = self.baseline_clinical_summary_cls.objects.filter(
            subject_identifier=OuterRef('subject_identifier'))

        appointment_obj = self.appointment_cls.objects.filter(
            appt_datetime__lte=get_utcnow().date(),
            appt_status='New',
            subject_identifier=OuterRef('subject_identifier'))

        '''
        cancer_probability_rank in order to sort values
        '''

        cancer_probability_rank = Case(
            When(cancer_probability__isnull=True, then=Value(0)),
            When(cancer_probability='low', then=Value(1)),
            When(cancer_probability='moderate', then=Value(2)),
            When(cancer_probability='high', then=Value(3)),
            default=Value(-1),
            output_field=CharField()
        )

        return super().get_queryset().annotate(
            cancer_probability=Subquery(
                base_clinical_summary.values('cancer_probability')[:1]
            ),
            specialist_appointment_date=Subquery(
                appointment_obj.values('appt_datetime')[:1]
            ),
            cancer_probability_rank=cancer_probability_rank,

        )


class WorkList(WorkListModelMixin):

    """A model linked to the subject consent to record corrections.
    """
    objects = WorklistManager()

    class Meta:
        app_label = 'potlako_follow'
        verbose_name = 'Worklist'
