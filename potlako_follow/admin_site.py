from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):
    site_title = 'Potlako Follow'
    site_header = 'Potlako Follow'
    index_title = 'Potlako Follow'
    site_url = '/administration/'
    enable_nav_sidebar = False

potlako_follow_admin = AdminSite(name='potlako_follow_admin')
