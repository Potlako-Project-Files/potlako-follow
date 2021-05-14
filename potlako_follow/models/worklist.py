from edc_search.model_mixins import SearchSlugManager
from .worklist_model_mixin import WorkListModelMixin, BaseWorkManager


class WorklistManager(BaseWorkManager, SearchSlugManager):
    pass


class WorkList(WorkListModelMixin):

    """A model linked to the subject consent to record corrections.
    """

    objects = WorklistManager()

    class Meta:
        app_label = 'potlako_follow'
        verbose_name = 'Worklist'
