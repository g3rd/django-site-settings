from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from parler.admin import TranslatableAdmin, TranslatableModelForm
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin, PolymorphicChildModelFilter
from site_settings import models


@admin.register(models.Key)
class KeyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'allow_multiples', )
    list_display_links = ('id', )
    list_editable = ('name', 'description', 'allow_multiples', )
    search_fields = ('name', )

    fieldsets = (
        (None, {'fields': ('name', 'description', 'allow_multiples', ), }),
    )


class SettingValueAdmin(TranslatableAdmin, PolymorphicChildModelAdmin):
    base_model = models.Setting
    base_form = TranslatableModelForm
    base_field = (
        'site', 'key', 'weight',
    )



@admin.register(models.Setting)
class SettingAdmin(TranslatableAdmin, PolymorphicParentModelAdmin):
    base_model = models.Setting
    child_models = (
        (models.CharSetting, SettingValueAdmin),
        (models.TextSetting, SettingValueAdmin),
        (models.DateTimeSetting, SettingValueAdmin),
        (models.DateSetting, SettingValueAdmin),
        (models.TimeSetting, SettingValueAdmin),
        (models.BooleanSetting, SettingValueAdmin),
        (models.NumberSetting, SettingValueAdmin),
        (models.DecimalSetting, SettingValueAdmin),
        (models.EmailSetting, SettingValueAdmin),
        (models.SlugSetting, SettingValueAdmin),
        (models.URLSetting, SettingValueAdmin),
    )

    def show_type(self, setting):
        return setting._meta.verbose_name
    show_type.short_description = _('type')

    polymorphic_list = True
    list_display = ('site_name', 'key', 'language_column', 'show_type')
    list_filter = (PolymorphicChildModelFilter, )
