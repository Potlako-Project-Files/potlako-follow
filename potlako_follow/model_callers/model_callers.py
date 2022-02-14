from potlako_subject.models import SubjectLocator

from django.core.exceptions import ValidationError
from edc_constants.constants import CLOSED, YES, NO

from edc_call_manager.decorators import register
from edc_call_manager.model_caller import ModelCaller, DAILY, OPEN_CALL

from ..models import Call, Log, LogEntry
from ..models import NavigationWorkList, WorkList


@register(WorkList)
class WorkListFollowUpModelCaller(ModelCaller):
    call_model = Call
    log_model = Log
    log_entry_model = LogEntry
    locator_model = (SubjectLocator, 'subject_identifier')
#     consent_model = (SubjectConsent, 'subject_identifier')
    log_entry_model = LogEntry
    log_model = Log
    interval = DAILY

    def update_call_from_log(self, call, log_entry, commit=True):
        """Updates the call_model instance with information from the log entry
        for this subject and model caller.

        Only updates call if this is the most recent log_entry."""
        log_entries = self.log_entry_model.objects.filter(
            log=log_entry.log).order_by('-call_datetime')
        if log_entry.pk == log_entries[0].pk:
            call = self.call_model.objects.get(pk=call.pk)
            if call.call_status == CLOSED:
                raise ValidationError(
                    'Call is closed. Perhaps catch this in the form.')
            if log_entry.outcome:
                call.call_outcome = '. '.join(log_entry.outcome)
            else:
                call.call_outcome = None
            call.call_datetime = log_entry.call_datetime
            call.call_attempts = log_entries.count()
            if log_entry.patient_reached == YES:
                call.call_status = CLOSED
            else:
                call.call_status = OPEN_CALL
            call.modified = log_entry.modified
            call.user_modified = log_entry.user_modified
            if commit:
                call.save()


@register(NavigationWorkList)
class NavigationWorkListFollowUpModelCaller(ModelCaller):
    call_model = Call
    log_model = Log
    log_entry_model = LogEntry
    locator_model = (SubjectLocator, 'subject_identifier')
#     consent_model = (SubjectConsent, 'subject_identifier')
    log_entry_model = LogEntry
    log_model = Log
    interval = DAILY

    def update_call_from_log(self, call, log_entry, commit=True):
        """Updates the call_model instance with information from the log entry
        for this subject and model caller.

        Only updates call if this is the most recent log_entry."""
        log_entries = self.log_entry_model.objects.filter(
            log=log_entry.log).order_by('-call_datetime')
        if log_entry.pk == log_entries[0].pk:
            call = self.call_model.objects.get(pk=call.pk)
            if call.call_status == CLOSED:
                raise ValidationError(
                    'Call is closed. Perhaps catch this in the form.')
            if log_entry.outcome:
                call.call_outcome = '. '.join(log_entry.outcome)
            call.call_datetime = log_entry.call_datetime
            call.call_attempts = log_entries.count()
            if log_entry.patient_reached == YES:
                call.call_status = CLOSED
            else:
                call.call_status = OPEN_CALL
            call.modified = log_entry.modified
            call.user_modified = log_entry.user_modified
            if commit:
                call.save()
