from django.db import models
from django_comments.abstracts import CommentAbstractModel
from django_comments.managers import CommentManager
from django.contrib.sites.models import Site


class InternalExternalCommentManager(CommentManager):
    def for_site(self, site=None):
        if site is None:
            site = Site.objects.get_current()

        return self.filter(site=site)

    def valid(self):
        return self.for_site().filter(is_removed=False, is_public=True)


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

    objects = InternalExternalCommentManager()

    class Meta(object):
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return "{}: {}".format(self.user or self.user_name, self.comment)

    @property
    def is_internal(self):
        return self.internal_external == self.INTERNAL
