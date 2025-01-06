from django.db import models
from django.utils.translation import gettext_lazy as _

class VoteData(models.Model):
    class HouseChoices(models.TextChoices):
        LYCEUM = 'l', _('Lyceum')
        PARNASSUS = 'p', _('Parnassus')
        VIRTUS = 'v', _('Virtus')

    house = models.CharField(
        max_length=1,
        choices=HouseChoices.choices,
        verbose_name=_('House')
    )
    visitor_ip = models.GenericIPAddressField(_('Visitor IP'), protocol='both', unpack_ipv4=True, null=True, blank=True)
    creation_time = models.DateTimeField(_('Creation time'), auto_now_add=True)
    last_modified_time = models.DateTimeField(_('Last modified time'), auto_now=True)

    class Meta:
        verbose_name = _('Vote Data')
        verbose_name_plural = _('Vote Data')
        ordering = ['-creation_time']

    def __str__(self):
        return f"{self.get_house_display()} ({self.visitor_ip})"

