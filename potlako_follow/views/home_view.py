from django.contrib.auth.decorators import login_required
from django.urls.base import reverse
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin


class HomeView(
        EdcBaseViewMixin, NavbarViewMixin,
        TemplateView):

    template_name = 'potlako_follow/home.html'
    navbar_name = 'potlako_follow'
    navbar_selected_item = 'potlako_follow'

    def get_success_url(self):
        return reverse('potlako_follow:home_url')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context.update()
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
