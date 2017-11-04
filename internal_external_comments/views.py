from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse

from internal_external_comments.models import InternalExternalComment
from internal_external_comments.forms import InternalExternalCommentForm


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response


# Create your views here.
class CommentDetail(AjaxableResponseMixin, DetailView):
    template_name = "internal_external_comments/detail.html"
    model = InternalExternalComment
    fields = '__all__'


class CommentCreate(AjaxableResponseMixin, CreateView):
    template_name = 'internal_external_comments/form.html'
    model = InternalExternalComment
    form_class = InternalExternalCommentForm


class CommentUpdate(AjaxableResponseMixin, UpdateView):
    template_name = 'internal_external_comments/form.html'
    model = InternalExternalComment
    form_class = InternalExternalCommentForm


class CommentDelete(AjaxableResponseMixin, DeleteView):
    pass
    # def get_object(self, queryset=None):
    #     """ Hook to ensure object is owned by request.user. """
    #     obj = super(CommentDeleteView, self).get_object()
    #     if not obj.owner == self.request.user:
    #         raise Http404
    #     return obj


class CommentList(AjaxableResponseMixin, ListView):
    model = InternalExternalComment
    template_name = 'internal_external_comments/list.html'
    fields = '__all__'


class CommentObjectListView(ListView):
    model = InternalExternalComment
    template_name = 'internal_external_comments/list.html'
    fields = '__all__'

    def get_queryset(self):
        return InternalExternalComment.objects.filter(
            django_content_type__app_label=self.kwargs['app_label'],
            django_content_type__model=self.kwargs['model'],
            object_pk=self.kwargs['object_pk'],
        )
