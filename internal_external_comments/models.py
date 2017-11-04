from django.db import models
from django_comments.abstracts import CommentAbstractModel
from django_comments.managers import CommentManager


class InternalExternalComment(CommentAbstractModel):
    INTERNAL = 'internal'
    EXTERNAL = 'external'
    INTERNAL_EXTERNAL_CHOICES = (
        (INTERNAL, 'Internal'),
        (EXTERNAL, 'External'),
    )
    internal_external = models.CharField(max_length=8,
                                         choices=INTERNAL_EXTERNAL_CHOICES,
                                         default=INTERNAL,)

    objects = CommentManager()

    class Meta(object):
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    @property
    def is_internal(self):
        return self.internal_external == self.INTERNAL
