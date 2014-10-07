from __future__ import unicode_literals
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from parler.managers import TranslatableManager, TranslatableQuerySet
from parler.models import TranslatableModel, TranslatedFields
from polymorphic import PolymorphicManager
from polymorphic import PolymorphicModel
from polymorphic.query import PolymorphicQuerySet


class SettingQuerySet(TranslatableQuerySet, PolymorphicQuerySet):
    pass


class SettingManager(PolymorphicManager, TranslatableManager):
    queryset_class = SettingQuerySet


@python_2_unicode_compatible
class Key(models.Model):
    name = models.CharField(_('name'), max_length=140, unique=True, db_index=True)
    description = models.TextField(_('description'), blank=True, null=True)
    allow_multiples = models.BooleanField(_('allow multiples per site?'), default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('key')
        verbose_name_plural = _('keys')
        ordering = ('name', )


@python_2_unicode_compatible
class Setting(PolymorphicModel, TranslatableModel):
    """
    A setting for a site
    """

    site = models.ForeignKey(Site)
    key = models.ForeignKey(Key, error_messages={
        'too_many_for_key': _("The %(key_name)s only allows a single value per site."),
    })
    weight = models.IntegerField(_('weight'), default=0)

    objects = SettingManager()

    def __str__(self):
        return '{} {}'.format(self.site.name, self.key.name)

    def site_name(self):
        return self.site.name
    site_name.short_description = _('site')
    site_name.admin_order_field = 'site__name'

    def clean(self, *args, **kwargs):
        super(Setting, self).clean(*args, **kwargs)

        if self.key.allow_multiples:
            return

        errors = {}

        settings_count = Setting.objects.filter(site=self.site, key=self.key).exclude(pk=self.pk).count()

        if settings_count > 0:
            err = ValidationError(
                message=self.key.field.error_messages['too_many_for_key'],
                code='too_many_for_key',
                params={
                    'key_name': self.key.name,
                },
            )
            errors.setdefault('key', []).append(err)

        if errors:
            raise ValidationError(errors)

    class Meta:
        verbose_name = _('Site setting')
        verbose_name_plural = _('Site settings')
        ordering = ('site', 'key', '-weight', )
        index_together = ['site', 'key']


class CharSetting(Setting):
    translations = TranslatedFields(
        value = models.CharField(_('value'), max_length=140)
    )

    class Meta:
        verbose_name = _('short text')
        verbose_name_plural = _('short text')


class DateTimeSetting(Setting):
    value = models.DateTimeField(_('value'))
    translations = TranslatedFields()

    class Meta:
        verbose_name = _('date and time')
        verbose_name_plural = _('date and time')


class DateSetting(Setting):
    value = models.DateField(_('value'))
    translations = TranslatedFields()

    class Meta:
        verbose_name = _('date')
        verbose_name_plural = _('date')


class TimeSetting(Setting):
    value = models.TimeField(_('value'))
    translations = TranslatedFields()

    class Meta:
        verbose_name = _('time')
        verbose_name_plural = _('time')


class BooleanSetting(Setting):
    value = models.BooleanField(_('value'), default=True)
    translations = TranslatedFields()

    class Meta:
        verbose_name = _('boolean')
        verbose_name_plural = _('boolean')


class NumberSetting(Setting):
    value = models.IntegerField(_('value'))
    translations = TranslatedFields()

    class Meta:
        verbose_name = _('number')
        verbose_name_plural = _('number')


class DecimalSetting(Setting):
    value = models.DecimalField(_('value'), decimal_places=4, max_digits=9)
    translations = TranslatedFields()

    class Meta:
        verbose_name = _('decimal')
        verbose_name_plural = _('decimal')


class TextSetting(Setting):
    translations = TranslatedFields(
        value = models.TextField(_('value'))
    )

    class Meta:
        verbose_name = _('text')
        verbose_name_plural = _('text')


class EmailSetting(Setting):
    value = models.EmailField(_('value'), max_length=254)
    translations = TranslatedFields()

    class Meta:
        verbose_name = _('email')
        verbose_name_plural = _('email')


class SlugSetting(Setting):
    translations = TranslatedFields(
        value = models.SlugField(_('value'), max_length=140)
    )

    class Meta:
        verbose_name = _('slug')
        verbose_name_plural = _('slug')


class URLSetting(Setting):
    translations = TranslatedFields(
        value = models.URLField(_('value'), max_length=2048)
    )

    class Meta:
        verbose_name = _('URL')
        verbose_name_plural = _('URL')
