import random

from django.contrib.auth.decorators import login_required
from django.urls.base import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin

from ..models import WorkList
from ..forms import AssignParticipantForm, ResetAssignmentForm


class HomeView(
        EdcBaseViewMixin, NavbarViewMixin,
        TemplateView, FormView):

    form_class = AssignParticipantForm
    template_name = 'potlako_follow/home.html'
    navbar_name = 'potlako_follow'
    navbar_selected_item = 'potlako_follow'

    @property
    def available_participants(self):
        available = WorkList.objects.filter(
            is_called=False, date_assigned__isnull=True, assigned__isnull=True).values_list(
                'subject_identifier', flat=True)
        return list(set(available))

    @property
    def participants_assignments(self):
        """Return participants assignments.
        """
        assignments = WorkList.objects.filter(
            date_assigned=timezone.now().date()).values_list(
                'assigned', 'study_maternal_identifier',)
        return assignments

    def reset_participant_assignments(self, username=None):
        """Resets all assignments if reset is yes.
        """
        if username == 'all':
            WorkList.objects.filter(
                date_assigned__isnull=False,
                assigned__isnull=False).update(
                    assigned=None, date_assigned=None)
        else:
            WorkList.objects.filter(
                date_assigned__isnull=False,
                assigned=username).update(
                    assigned=None, date_assigned=None)
    
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        if form.is_valid():
            selected_participants = []
            username = form.cleaned_data['username']
            participants = form.cleaned_data['participants']
            if len(self.available_participants) < participants:
                selected_participants = self.available_participants
            else:
                selected_participants = random.sample(
                    self.available_participants, participants)
            self.create_user_worklist(
                username=username, selected_participants=selected_participants)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('potlako_follow:home_url')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reset_assignment_form = ResetAssignmentForm()
        if self.request.method == 'POST':
            reset_assignment_form = ResetAssignmentForm(self.request.POST)
            if reset_assignment_form.is_valid():
                username = reset_assignment_form.data['username']
                self.reset_participant_assignments(username=username)
        context.update(
            total_assigned=len(self.participants_assignments),
            available_participants=len(self.available_participants),
            successful_calls=WorkList.objects.filter(is_called=True).count(),
            reset_assignment_form=reset_assignment_form)
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
