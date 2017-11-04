from django import forms
from django_comments.forms import CommentForm

from .models import InternalExternalComment
from .widgets import InternalExternalTextBoxWidget


class InternalExternalCommentForm(CommentForm):
    comment = forms.CharField(required=True, initial="",
                              widget=InternalExternalTextBoxWidget())
    internal_external = forms.CharField(required=True, initial="internal",
                                        widget=forms.HiddenInput())

    def __init__(self, target_object, data=None, initial=None, **kwargs):
        super(InternalExternalCommentForm, self).__init__(
            target_object=target_object, data=data, initial=initial, **kwargs)
        if 'internal_external' not in self.initial:
            self.initial['internal_external'] = 'internal'

    def get_comment_model(self):
        return InternalExternalCommentForm

    def get_comment_create_data(self):
        data = super(InternalExternalCommentForm, self).get_comment_create_data()
        data['internal_external'] = self.cleaned_data['internal_external']
        return data

    def get_comment_object(self):
        if not self.is_valid():
            raise ValueError("get_comment_object may only be called on valid forms")

        return InternalExternalComment(**self.get_comment_create_data())
