from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CustomAppConfig(AppConfig):
    name = 'site_settings'
    verbose_name = _('Site setting')
    verbose_name_plural = _('Site settings')
