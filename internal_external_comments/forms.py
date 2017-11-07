from django import forms
from django_comments.forms import CommentForm

from .models import InternalExternalComment
from .widgets import InternalExternalTextBoxWidget


class InternalExternalCommentForm(CommentForm):
    comment = forms.CharField(required=True, initial="",
                              widget=InternalExternalTextBoxWidget())
    internal_external = forms.CharField(required=True, initial="internal",
                                        widget=forms.HiddenInput())

    def __init__(self, target_object=None, data=None, initial=None, **kwargs):
        if initial is None:
            initial = {}
        self.internal_external = initial.get('internal_external')
        if data is not None:
            self.internal_external = data.get('internal_external')
        if self.internal_external is None:
            self.internal_external = "internal"
        if data is not None:
            data.update({'internal_external': self.internal_external})
        initial.update({'internal_external': self.internal_external})
        super(InternalExternalCommentForm, self).__init__(
            target_object=target_object, data=data, initial=initial, **kwargs)
        self.fields['comment'].widget.internal_external = self.internal_external

    def get_comment_model(self, *args, **kwargs):
        return InternalExternalCommentForm

    def get_comment_create_data(self, *args, **kwargs):
        data = super(InternalExternalCommentForm, self).get_comment_create_data(*args, **kwargs)
        data['internal_external'] = self.cleaned_data['internal_external']
        return data

    def get_comment_object(self, *args, **kwargs):
        if not self.is_valid():
            raise ValueError("get_comment_object may only be called on valid forms")

        return InternalExternalComment(**self.get_comment_create_data(*args, **kwargs))
