from edc_search.model_mixins import SearchSlugManager
from .worklist_model_mixin import WorkListModelMixin, BaseWorkManager


class InvestigationFUWorklistManager(BaseWorkManager, SearchSlugManager):
    pass


class InvestigationFUWorkList(WorkListModelMixin):

    """A model linked to the investigations ordered form to record corrections.
    """

    objects = InvestigationFUWorklistManager()

    class Meta:
        app_label = 'potlako_follow'
        verbose_name = 'Investigation Follow Up Worklist'
