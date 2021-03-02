from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings


class AppConfig(DjangoAppConfig):
    name = 'potlako_follow'
    verbose_name = 'Potlako Follow'
    admin_site_name = 'potlako_follow_admin'
    extra_assignee_choices = ()
    assignable_users_group = 'assignable users'

    def ready(self):
        pass
#         from .models import cal_log_entry_on_post_save
#         from .models import worklist_on_post_save


if settings.APP_NAME == 'potlako_follow':

    from datetime import datetime
    from dateutil.tz import gettz

    from edc_appointment.appointment_config import AppointmentConfig
    from edc_appointment.apps import AppConfig as BaseEdcAppointmentAppConfig
    from edc_appointment.constants import COMPLETE_APPT
    from edc_protocol.apps import AppConfig as BaseEdcProtocolAppConfigs
    from edc_timepoint.apps import AppConfig as BaseEdcTimepointAppConfig
    from edc_timepoint.timepoint import Timepoint
    from edc_timepoint.timepoint_collection import TimepointCollection
    from edc_visit_tracking.apps import (
        AppConfig as BaseEdcVisitTrackingAppConfig)

    class EdcAppointmentAppConfig(BaseEdcAppointmentAppConfig):
        configurations = [
            AppointmentConfig(
                model='edc_appointment.appointment',
                related_visit_model='potlako_subject.subjectvisit',
                appt_type='clinic')]

    class EdcProtocolAppConfig(BaseEdcProtocolAppConfigs):
        protocol = 'BHP0135'
        protocol_name = 'Potlako Follow'
        protocol_number = '132'
        protocol_title = ''
        study_open_datetime = datetime(
            2016, 4, 1, 0, 0, 0, tzinfo=gettz('UTC'))
        study_close_datetime = datetime(
            2020, 12, 1, 0, 0, 0, tzinfo=gettz('UTC'))

    class EdcTimepointAppConfig(BaseEdcTimepointAppConfig):
        timepoints = TimepointCollection(
            timepoints=[
                Timepoint(
                    model='edc_appointment.appointment',
                    datetime_field='appt_datetime',
                    status_field='appt_status',
                    closed_status=COMPLETE_APPT),
                Timepoint(
                    model='edc_appointment.historicalappointment',
                    datetime_field='appt_datetime',
                    status_field='appt_status',
                    closed_status=COMPLETE_APPT),
            ])

    class EdcVisitTrackingAppConfig(BaseEdcVisitTrackingAppConfig):
        visit_models = {
            'potlako_subject': (
                'subject_visit', 'potlako_subject.subjectvisit'),}
