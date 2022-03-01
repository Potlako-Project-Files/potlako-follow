import imp
from django.db import models
from edc_search.model_mixins import SearchSlugManager
from .worklist_model_mixin import WorkListModelMixin, BaseWorkManager
from django.apps import apps as django_apps
from queryable_properties.properties import queryable_property
from queryable_properties.managers import QueryablePropertiesManager
from potlako_subject.models import BaselineClinicalSummary
from django.db.models import Subquery, QuerySet, OuterRef, Count

class WorklistManager(BaseWorkManager, SearchSlugManager):
    def get_queryset(self):

        base_clinical_summary = BaselineClinicalSummary.objects.filter(
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
