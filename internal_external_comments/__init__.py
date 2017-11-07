"""
These are required from django_comments app
"""
__version__ = '0.1.0'


def get_model():
    from internal_external_comments.models import InternalExternalComment
    return InternalExternalComment


def get_form():
    from internal_external_comments.forms import InternalExternalCommentForm
    return InternalExternalCommentForm
