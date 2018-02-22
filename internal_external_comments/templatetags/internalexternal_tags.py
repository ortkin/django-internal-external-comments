from django.template import Node, TemplateSyntaxError, Variable
from django_comments.templatetags.comments import register, RenderCommentListNode
from django.contrib.contenttypes.models import ContentType
from internal_external_comments.forms import InternalExternalCommentForm
from internal_external_comments.views import CommentObjectListView  #, CommentCreateView
from django_comments.templatetags.comments import BaseCommentNode, CommentListNode, CommentFormNode


# @register.simple_tag(takes_context=True)
# def render_internal_external_comment_form(obj, *args, **kwargs):
#     return {'comment_form': InternalExternalCommentForm(obj)}


# @register.simple_tag(takes_context=True)
# def render_internal_external_comment_list(obj, *args, **kwargs):
#     def __init__(self, target_object, args, kwargs):
#         self.target_object = target_object
#         self.args = args
#         self.kwargs = kwargs

#     def render(self, context):
#         return CommentObjectListView.as_view()(self.target_object, context['request'].user)


# class CommentsFormViewNode(BaseCommentNode):
#     def __init__(self, target_object):
#         self.target_object = target_object

#     def render(self, context):
#         obj = Variable(self.target_object).resolve(context)
#         # print(dir(obj))
#         view = CommentCreateView.as_view()
#         return view(obj, context['request']).content


# @register.tag()
# def get_internal_external_form(parser, token):
#     """
#     {% comment_form for [object] %}
#     """
#     try:
#         tag_name, mustbefor, target_object = token.split_contents()
#         if mustbefor != 'for':
#             raise TemplateSyntaxError("Second argument in %r tag must be 'for'" % mustbefor)
#     except ValueError:
#         raise TemplateSyntaxError("comments_form should be in the form: "
#                                   "{% comments_form target_object %}")
#     return CommentsFormViewNode(target_object)


@register.tag
def get_comment_list(parser, token):
    """
    Gets the list of comments for the given params and populates the template
    context with a variable containing that value, whose name is defined by the
    'as' clause.
    Syntax::
        {% get_comment_list for [object] as [varname]  %}
    Example usage::
        {% get_comment_list for event as comment_list %}
        {% for comment in comment_list %}
            ...
        {% endfor %}
    """
    return CommentListNode.handle_token(parser, token)
