from django.conf import settings

from edc_navbar import NavbarItem, site_navbars, Navbar

potlako_follow = Navbar(name='potlako_follow')
no_url_namespace = True if settings.APP_NAME == 'potlako_follow' else False

potlako_follow.append_item(
    NavbarItem(name='potlako_follow',
               label='Potlako follow',
               fa_icon='fa-cogs',
               url_name='potlako_follow:home_url'))

potlako_follow.append_item(
    NavbarItem(
        name='worklist',
        title='Worklist',
        label='Worklist',
        fa_icon='fa-user-plus',
        url_name=settings.DASHBOARD_URL_NAMES[
            'potlako_follow_listboard_url'],
        no_url_namespace=no_url_namespace))

site_navbars.register(potlako_follow)
