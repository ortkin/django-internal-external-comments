from django import forms
from django.core.exceptions import ImproperlyConfigured
from django_comments.forms import CommentForm

from .models import InternalExternalComment
from .widgets import InternalExternalTextBoxWidget


class InternalExternalCommentForm(CommentForm):
    comment = forms.CharField(required=True, initial="",
                              widget=InternalExternalTextBoxWidget())
    internal_external = forms.CharField(required=True, initial="internal",
                                        widget=forms.HiddenInput())

    def __init__(self, target_object, data=None, initial=None, request=None, **kwargs):
        try:
            self.target_object = target_object
        except Exception:
            raise ImproperlyConfigured('Comment form must be passed a target/parent object.')
        if request is None:
            raise ImproperlyConfigured('Comment form must be passed the request object.')
        try:
            user = request.user
        except Exception:
            raise ImproperlyConfigured('Request object passed to comment must contain a user object.')
        internal_external = 'internal'
        if initial is None:
            initial = {}
        else:
            internal_external = initial.get('internal_external', 'internal')
        if data is not None:
            internal_external = data.get('internal_external', 'internal')
        if not user.has_perm('internal_external_comments.can_post_internal'):
            internal_allow = False
            internal_external = "external"
        else:
            internal_allow = True
        initial.update({'internal_external': internal_external})
        if data is not None:
            data.update({'internal_external': internal_external})
        super(InternalExternalCommentForm, self).__init__(
            target_object=target_object, data=data, initial=initial, **kwargs)
        self.fields['comment'].widget.internal_external = internal_external
        self.fields['comment'].widget.internal_allow = internal_allow

    def get_comment_model(self, *args, **kwargs):
        return InternalExternalComment

    def get_comment_create_data(self, *args, **kwargs):
        data = super(InternalExternalCommentForm, self).get_comment_create_data(*args, **kwargs)
        data['internal_external'] = self.cleaned_data['internal_external']
        return data

    def get_comment_object(self, *args, **kwargs):
        if not self.is_valid():
            raise ValueError("get_comment_object may only be called on valid forms")

        return InternalExternalComment(**self.get_comment_create_data(*args, **kwargs))
