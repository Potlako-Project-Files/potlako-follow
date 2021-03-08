from django.db import models

from edc_base.model_mixins import BaseUuidModel
from multiselectfield import MultiSelectField

from edc_base.model_fields import OtherCharField
from edc_base.model_validators import date_is_future, datetime_not_future
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO_NA
from edc_constants.constants import YES, NOT_APPLICABLE

from edc_call_manager.model_mixins import (
    CallModelMixin, LogModelMixin, LogEntryModelMixin)

from ..choices import (
    APPT_GRADING, APPT_LOCATIONS, APPT_REASONS_UNWILLING,
    CONTACT_FAIL_REASON, MAY_CALL, PHONE_USED, PHONE_SUCCESS,
    HOME_VISIT)


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

    phone_num_type = MultiSelectField(
        verbose_name='Which phone number(s) was used for contact?',
        choices=PHONE_USED)

    phone_num_success = MultiSelectField(
        verbose_name='Which number(s) were you successful in reaching?',
        choices=PHONE_SUCCESS)

    cell_contact_fail = models.CharField(
        verbose_name='Why was the contact to [ ] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON,
        default=NOT_APPLICABLE)

    alt_cell_contact_fail = models.CharField(
        verbose_name='Why was the contact to [ ] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON,
        default=NOT_APPLICABLE)

    tel_contact_fail = models.CharField(
        verbose_name='Why was the contact to [ ] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON,
        default=NOT_APPLICABLE)

    alt_tel_contact_fail = models.CharField(
        verbose_name='Why was the contact to [ ] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON,
        default=NOT_APPLICABLE)

    work_contact_fail = models.CharField(
        verbose_name='Why was the contact to [ ] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON,
        default=NOT_APPLICABLE)

    cell_alt_contact_fail = models.CharField(
        verbose_name='Why was the contact to [ ] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON,
        default=NOT_APPLICABLE)

    tel_alt_contact_fail = models.CharField(
        verbose_name='Why was the contact to [ ] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON,
        default=NOT_APPLICABLE)

    cell_resp_person_fail = models.CharField(
        verbose_name='Why was the contact to [ ] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON,
        default=NOT_APPLICABLE)

    tel_resp_person_fail = models.CharField(
        verbose_name='Why was the contact to [ ] unsuccessful?',
        max_length=100,
        choices=CONTACT_FAIL_REASON,
        default=NOT_APPLICABLE)

    appt = models.CharField(
        verbose_name='Is the participant willing to schedule an appointment',
        max_length=7,
        choices=YES_NO_NA)

    appt_reason_unwilling = models.CharField(
        verbose_name='What is the reason the participant is unwilling to schedule an appointment',
        max_length=25,
        choices=APPT_REASONS_UNWILLING,
        null=True,
        blank=True)

    appt_reason_unwilling_other = models.CharField(
        verbose_name='Other reason, please specify ...',
        max_length=50,
        null=True,
        blank=True)

    appt_date = models.DateField(
        verbose_name="Appointment Date",
        validators=[date_is_future],
        null=True,
        blank=True,
        help_text="This can only come from the participant.")

    appt_grading = models.CharField(
        verbose_name='Is this appointment...',
        max_length=25,
        choices=APPT_GRADING,
        null=True,
        blank=True)

    appt_location = models.CharField(
        verbose_name='Appointment location',
        max_length=50,
        choices=APPT_LOCATIONS,
        null=True,
        blank=True)

    appt_location_other = OtherCharField(
        verbose_name='Other location, please specify ...',
        max_length=50,
        null=True,
        blank=True)

    delivered = models.BooleanField(
        null=True,
        default=False,
        editable=False)

    may_call = models.CharField(
        verbose_name='May we continue to contact the participant?',
        max_length=10,
        choices=MAY_CALL,
        default=YES)

    home_visit = models.CharField(
        verbose_name='Perform home visit.',
        max_length=50,
        choices=HOME_VISIT,
        default=NOT_APPLICABLE)

    home_visit_other = models.CharField(
        verbose_name='Other reason, please specify ...',
        max_length=50,
        null=True,
        blank=True)

    class Meta(LogEntryModelMixin.Meta):
        app_label = 'potlako_follow'