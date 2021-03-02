from edc_call_manager.model_caller import ModelCaller, DAILY
from edc_call_manager.decorators import register

from potlako_subject.models import SubjectLocator

from edc_call_manager.models import Call, Log, LogEntry
from ..models import WorkList


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
