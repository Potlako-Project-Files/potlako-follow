from django.apps import apps as django_apps
from django.db import models
from django.db.models import Subquery, OuterRef
from django.db.models import When, Case, Value, CharField
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators.date import datetime_not_future, date_not_future
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_search.model_mixins import SearchSlugModelMixin


class BaseWorkManager(models.Manager):

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

    def get_by_natural_key(self, subject_identifier):
        return self.get(subject_identifier=subject_identifier)


class WorkListModelMixin(SiteModelMixin, SearchSlugModelMixin, BaseUuidModel):

    """A base model for creating worklists.
    """

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50,
        null=True,
        blank=True,
        unique=True)

    report_datetime = models.DateTimeField(
        verbose_name="Report date ad time",
        null=True,
        validators=[
            datetime_not_future],
    )

    assigned = models.CharField(
        verbose_name='User assigned',
        max_length=250,
        null=True)

    date_assigned = models.DateField(
        verbose_name="Date assigned",
        null=True,
        validators=[
            date_not_future],
    )

    is_called = models.BooleanField(default=False)

    called_datetime = models.DateTimeField(null=True)

    visited = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.subject_identifier}'

    def natural_key(self):
        return (self.subject_identifier,)

    def get_search_slug_fields(self):
        fields = ['subject_identifier', ]
        return fields

    class Meta:
        app_label = 'potlako_follow'
        abstract = True
