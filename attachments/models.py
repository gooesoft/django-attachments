from __future__ import unicode_literals

import os

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


def attachment_upload(instance, filename):
    """Stores the attachment in a "per module/appname/primary key" folder"""
    return 'attachments/{app}_{model}/{pk}/{filename}'.format(
        app=instance.content_object._meta.app_label,
        model=instance.content_object._meta.object_name.lower(),
        pk=instance.content_object.pk,
        filename=filename)


class AttachmentManager(models.Manager):
    def attachments_for_object(self, obj, category):
        object_type = ContentType.objects.get_for_model(obj)
        return self.filter(content_type__pk=object_type.id,
                           object_id=obj.pk,
                           category=category)


@python_2_unicode_compatible
class Attachment(models.Model):
    INVOICE = 'INVOICE'
    RECEIPT = 'RECEIPT'
    DEFAULT = 'FILE'

    TYPES = (
        (DEFAULT, 'File'),
        (INVOICE, 'Invoice'),
        (RECEIPT, 'Receipt'),
    )

    objects = AttachmentManager()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.BigIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="created_attachments",
                                verbose_name=_('creator'), on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False)
    attachment_file = models.FileField(_('attachment'), upload_to=attachment_upload)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    category = models.CharField(default=DEFAULT, max_length=30)

    class Meta:
        verbose_name = _("attachment")
        verbose_name_plural = _("attachments")
        ordering = ['-created']
        permissions = (
            ('delete_foreign_attachments', _('Can delete foreign attachments')),
        )

    def __str__(self):
        return _('{username} attached {name}').format(
            username=self.creator,
            name=self.name
        )

    @property
    def filename(self):
        return os.path.split(self.attachment_file.name)[1]

    def url(self):
        """
        Returns relative URL of the attachment file, which already includes MEDIA_URL value
        """
        return os.path.join(self.attachment_file.storage.base_url, self.attachment_file.name)
