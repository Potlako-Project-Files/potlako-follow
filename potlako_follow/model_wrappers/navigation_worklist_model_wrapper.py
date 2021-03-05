from django.apps import apps as django_apps
from django.conf import settings

from potlako_dashboard.model_wrappers import (
    BaselineClinicalSummaryModelWrapperMixin, NavigationPlanSummaryModelWrapperMixin)
from edc_model_wrapper import ModelWrapper



class NavigationWorkListModelWrapper(
        BaselineClinicalSummaryModelWrapperMixin, NavigationPlanSummaryModelWrapperMixin,
         ModelWrapper):

    model = 'potlako_follow.navigationworklist'
    querystring_attrs = ['subject_identifier']
    next_url_attrs = ['subject_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'potlako_navigation_listboard_url')

    @property
    def community_arm(self):
        onschedule_model_cls = django_apps.get_model(
            'potlako_subject.onschedule')
        try:
            onschedule_obj = onschedule_model_cls.objects.get(
                subject_identifier=self.subject_identifier)
        except ObjectDoesNotExist:
            return None
        else:
            return onschedule_obj.community_arm