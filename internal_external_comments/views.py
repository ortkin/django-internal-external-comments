from django.contrib.contenttypes.models import ContentType
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from django_comments import views as comments_views

from internal_external_comments.models import InternalExternalComment
from internal_external_comments.forms import InternalExternalCommentForm


# Mixins.
class CommentObjectMixin(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ctype = ContentType.objects.get(
            app_label=self.kwargs['app_label'], model=self.kwargs['model'])
        context['target_content_type'] = ctype
        context['target_object'] = ctype.get_object_for_this_type(pk=self.kwargs['object_pk'])
        return context


class CommentFormMixin(object):
    template_name = 'internal_external_comments/form.html'
    model = InternalExternalComment
    form_class = InternalExternalCommentForm
    target_object = None
    target_content_type = None

    # def get_app_model_name(kwargs):
    #     app_name = kwargs.get('app_name').lower()
    #     model_name = kwargs.get('model_name').lower()
    #     return app_name, model_name

    # def get_model_content_type(app_name, model_name):
    #     return ContentType.objects.get(app_label=app_name, model=model_name)

    # def _get_target_object(self, app_label, model, object_id):
    #     self.target_content_type = ContentType.objects.get(app_label=app_label, model=model)
    #     try:
    #         return self.target_content_type.get_object_for_this_type(id=object_id)

    #     except ObjectDoesNotExist:
    #         raise Http404

    # def get_initial(self):
    #     initial = super().get_initial()

    #     content_type_pk = self.request.GET.get('content_type', None)
    #     content_type = ContentType.objects.get_for_id(content_type_pk) if content_type_pk else None
    #     object_pk = self.request.GET.get('object_pk', None)
    #     # find the related model
    #     model = content_type.get_object_for_this_type(**{'pk': object_pk}) if content_type and object_pk else None
    #     full_rating = model.full_rating(self.request.user) if model and model.rated_by(self.request.user) else None
    #     return {
    #         'content_type': content_type,
    #         'object_pk': object_pk,
    #         'rating': full_rating[0] if full_rating else self.request.GET.get('min_rate', 0),
    #         'user': self.request.user,
    #         'comment': full_rating[1] if full_rating else None,
    #     }

    # def dispatch(self, request, *args, **kwargs):
    #     self.app_label = kwargs.pop('app_label')
    #     self.model = kwargs.pop('model')
    #     self.object_pk = kwargs.get("object_pk", kwargs.get("object_id", None))

    #     # Raise 404 error if app_label and model does not exist!
    #     try:
    #         self.target_content_type = ContentType.objects.get(
    #             app_label=self.app_label, model=self.model)
    #         self.target_object = self.target_content_type.get_object_for_this_type(
    #             pk=self.object_pk)
    #     except ObjectDoesNotExist:
    #         raise ImproperlyConfigured(
    #             "{0} is missing a valid realm_content_type.".format(
    #                 self.__class__.__name__))
    #     return super().dispatch(request, *args, **kwargs)

    # def __init__(self, **kwargs):
    #     print(kwargs)
    #     if self.content_type is None:
    #         self.content_type = ContentType.objects.get(app_label=kwargs['app_label'], model=kwargs['model'])
    #     if kwargs.get("content_type_id", None) is not None:
    #         self.content_type = get_object_or_404(ContentType, pk=kwargs.get("content_type_id", None))
    #     self.content_object = self.content_type.get_object_for_this_type(pk=kwargs.get("object_pk", kwargs.get("object_id", None)))

    def post(self, request, *args, **kwargs):
        comments_views.post_comment(request)
        return super().post(request, *args, **kwargs)


class CommentDetailView(DetailView):
    template_name = "internal_external_comments/comment.html"
    model = InternalExternalComment
    fields = '__all__'


class CommentObjectCreateView(CommentObjectMixin, CommentFormMixin, CreateView):
    def get_form_kwargs(self):
        kwargs = super(CommentObjectCreateView, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
            'target_object': self.target_object,
        })
        return kwargs


class CommentUpdateView(CommentFormMixin, UpdateView):
    def get_form_kwargs(self):
        kwargs = super(CommentUpdateView, self).get_form_kwargs()
        kwargs.update({
            "request": self.request,
            "target_object": self.object.content_object,
        })
        return kwargs
    # def form_valid(self, form):
    #     if not self.object.user:
    #         return HttpResponse('not allowed')
    #     else:
    #         if (self.request.user.is_authenticated and
    #                 self.object.user == self.request.user):
    #             form.save()
    #             return super(CommentUpdateView, self).form_valid(form)
    #         else:
    #             return HttpResponse('not authenticated')


class CommentDeleteView(DeleteView):
    pass
    # def get_object(self, queryset=None):
    #     """ Hook to ensure object is owned by request.user. """
    #     obj = super(CommentDeleteView, self).get_object()
    #     if not obj.owner == self.request.user:
    #         raise Http404
    #     return obj


class CommentListView(ListView):
    model = InternalExternalComment
    template_name = 'internal_external_comments/list.html'
    fields = '__all__'


class CommentObjectListView(CommentObjectMixin, ListView):
    model = InternalExternalComment
    template_name = 'internal_external_comments/list.html'
    fields = '__all__'
    context_object_name = 'comment_list'

    def get_queryset(self):
        return InternalExternalComment.objects.filter(
            content_type__app_label=self.kwargs['app_label'],
            content_type__model=self.kwargs['model'],
            object_pk=self.kwargs['object_pk'],
        )
