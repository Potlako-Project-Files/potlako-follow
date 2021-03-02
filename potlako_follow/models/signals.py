from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models.worklist import WorkList
from edc_call_manager.models import LogEntry


@receiver(post_save, weak=False, sender=LogEntry,
          dispatch_uid="cal_log_entry_on_post_save")
def cal_log_entry_on_post_save(sender, instance, using, raw, **kwargs):
    if not raw:
        try:
            work_list = WorkList.objects.get(
                study_maternal_identifier=instance.study_maternal_identifier)
        except WorkList.DoesNotExist:
            pass
        else:
            if 'none_of_the_above' not in instance.phone_num_success:
                work_list.is_called = True
                work_list.called_datetime = instance.call_datetime
                work_list.save()
