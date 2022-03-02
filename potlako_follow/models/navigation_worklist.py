from edc_search.model_mixins import SearchSlugManager
from .worklist_model_mixin import WorkListModelMixin, BaseWorkManager
from django.db.models import OuterRef, Subquery
from potlako_subject.models import SubjectScreening, SubjectConsent, ClinicianCallEnrollment


class NavigationWorklistManager(BaseWorkManager, SearchSlugManager):
    def get_queryset(self):
        """
        - Naviagation Work list have no screening identifier
        - Screening Identifiers are calculated on the fly
        - Clinical call enrollment, contain the screening identifier, and subject
        identifier is blank, so the calculated screening identifier was used instead
        """

        screening_identifier = SubjectConsent.objects.filter(
            subject_identifier=OuterRef('subject_identifier'))

        village_town = ClinicianCallEnrollment.objects.filter(
            screening_identifier=OuterRef('screening_identifier')
        )

        

        return super().get_queryset().annotate(
            screening_identifier=Subquery(
                screening_identifier.values('screening_identifier')[:1]
            ),
            village_town = Subquery(
                village_town.values('village_town')[:1]
            )
        )


class NavigationWorkList(WorkListModelMixin):

    """A model linked to the navigation plan form to record corrections.
    """

    objects = NavigationWorklistManager()

    class Meta:
        app_label = 'potlako_follow'
        verbose_name = 'Navigation Worklist'
