# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from cms.cms_toolbar import ADMIN_MENU_IDENTIFIER, ADMINISTRATION_BREAK
from cms.toolbar.items import Break
from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


@toolbar_pool.register
class SiteSettingsToolbar(CMSToolbar):

    def populate(self):
        admin_menu = self.toolbar.get_or_create_menu(ADMIN_MENU_IDENTIFIER)
        position = admin_menu.find_first(Break, identifier=ADMINISTRATION_BREAK)
        url = reverse('admin:site_settings_setting_changelist')
        admin_menu.add_sideframe_item(_('Settings'), position=position, url=url)
