import imp
from django.db import models
from edc_search.model_mixins import SearchSlugManager
from urllib3 import Retry
from .worklist_model_mixin import WorkListModelMixin, BaseWorkManager
from django.apps import apps as django_apps
from queryable_properties.properties import queryable_property
from queryable_properties.managers import QueryablePropertiesManager
from potlako_subject.models import BaselineClinicalSummary
from django.db.models import Subquery, QuerySet, OuterRef, Count

class WorklistManager(BaseWorkManager, SearchSlugManager):

    baseline_clinical_summary_model = 'potlako_subject.baselineclinicalsummary'

    @property
    def baseline_clinical_summary_cls(self):
        return django_apps.get_model(self.baseline_clinical_summary_model)

    def get_queryset(self):

        """
        Overriding the queryset in order to include a calculated value
        so one can use filter on a calcuated property or attribute
        """

        base_clinical_summary = self.baseline_clinical_summary_cls.objects.filter(
                subject_identifier=OuterRef('subject_identifier'))

        return super().get_queryset().annotate(
            cancer_probability=Subquery(
                base_clinical_summary.values('cancer_probability')[:1]
            )
        )


class WorkList(WorkListModelMixin):

    """A model linked to the subject consent to record corrections.
    """
    objects = WorklistManager()

    class Meta:
        app_label = 'potlako_follow'
        verbose_name = 'Worklist'
