from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import datetime_not_future
from edc_base.utils import get_utcnow
from edc_call_manager.model_mixins import (
    CallModelMixin, LogModelMixin, LogEntryModelMixin)
from edc_constants.choices import YES_NO

from ..choices import CALL_OUTCOME


class Call(CallModelMixin, BaseUuidModel):

    class Meta(CallModelMixin.Meta):
        app_label = 'potlako_follow'


class Log(LogModelMixin, BaseUuidModel):

    call = models.ForeignKey(Call, on_delete=models.PROTECT)

    class Meta(LogModelMixin.Meta):
        app_label = 'potlako_follow'


class LogEntry(BaseUuidModel):

    log = models.ForeignKey(Log, on_delete=models.PROTECT)

    subject_identifier = models.CharField(
        max_length=50,
        blank=True,)

    call_datetime = models.DateTimeField(
        default=get_utcnow,
        validators=[datetime_not_future, ],
        verbose_name='Date of contact attempt')

    patient_reached = models.CharField(
        verbose_name='Was the patient reached?',
        choices=YES_NO,
        max_length=3,)

    call_outcome = models.CharField(
        verbose_name='If yes, what was the call outcome?',
        choices=CALL_OUTCOME,
        max_length=20,
        null=True,
        blank=True)

    @property
    def outcome(self):
        return self.call_outcome

    class Meta(LogEntryModelMixin.Meta):
        app_label = 'potlako_follow'
