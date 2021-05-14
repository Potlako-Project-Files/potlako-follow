from edc_search.model_mixins import SearchSlugManager
from .worklist_model_mixin import WorkListModelMixin, BaseWorkManager


class NavigationWorklistManager(BaseWorkManager, SearchSlugManager):
    pass


class NavigationWorkList(WorkListModelMixin):

    """A model linked to the navigation plan form to record corrections.
    """

    objects = NavigationWorklistManager()

    class Meta:
        app_label = 'potlako_follow'
        verbose_name = 'Navigation Worklist'
