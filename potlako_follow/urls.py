from django.urls import path

from edc_dashboard import UrlConfig
from .admin_site import potlako_follow_admin
from .views import ListboardView, HomeView


app_name = 'potlako_follow'

subject_identifier = '066\-[0-9\-]+'
screening_identifier = '[A-Z0-9]{8}'

urlpatterns = [
    path('admin/', potlako_follow_admin.urls),
    path('', HomeView.as_view(), name='home_url'),
]

potlako_follow_listboard_url_config = UrlConfig(
    url_name='potlako_follow_listboard_url',
    view_class=ListboardView,
    label='potlako_follow_listboard',
    identifier_label='subject_identifier',
    identifier_pattern=screening_identifier)

urlpatterns += potlako_follow_listboard_url_config.listboard_urls
