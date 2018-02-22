from django.db import models
from django_comments.abstracts import CommentAbstractModel
from django_comments.managers import CommentManager
from django.contrib.sites.models import Site
from django.urls import reverse


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
        permissions = (
            ("can_post_internal", "Can post internal message"),
            ("can_delete_internal", "Can delete internal message"),
            ("can_edit_internal", "Can edit internal message"),
            ("can_view_internal", "Can view internal message"),
            ("can_delete_external", "Can delete external message"),
            ("can_edit_external", "Can edit external message"),
        )

    def __str__(self):
        return "{}: {}".format(self.user or self.user_name, self.comment)

    @property
    def is_internal(self):
        return self.internal_external == self.INTERNAL

    @property
    def data(self):
        return {
            "pk": self.pk,
            "comment": self.comment,
            "user": self.user.username if self.user else "",
            "object_pk": self.object_pk,
            "content_type_id": self.content_type_id,
            "submit_date": str(self.submit_date),
        }

    def get_content_object_url(self):
        """
        Get a URL suitable for redirecting to the content object.
        """
        return reverse(
            "comments-url-redirect",
            args=(self.content_type_id, self.object_pk)
        )
