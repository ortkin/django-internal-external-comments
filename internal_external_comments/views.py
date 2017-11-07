from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse, HttpResponse

from django_comments import views as comments_views

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
class CommentDetailView(AjaxableResponseMixin, DetailView):
    template_name = "internal_external_comments/comment.html"
    model = InternalExternalComment
    fields = '__all__'


class CommentCreateView(AjaxableResponseMixin, CreateView):
    template_name = 'internal_external_comments/form.html'
    model = InternalExternalComment
    form_class = InternalExternalCommentForm

    def post(self, request, *args, **kwargs):
        comments_views.post_comment(request)


class CommentUpdateView(AjaxableResponseMixin, UpdateView):
    template_name = 'internal_external_comments/form.html'
    model = InternalExternalComment
    form_class = InternalExternalCommentForm

    def form_valid(self, form):
        if not self.object.user:
            return HttpResponse('not allowed')
        else:
            if (self.request.user.is_authenticated and
                    self.object.user == self.request.user):
                form.save()
                return super(CommentUpdateView, self).form_valid(form)
            else:
                return HttpResponse('not authenticated')


class CommentDeleteView(AjaxableResponseMixin, DeleteView):
    pass
    # def get_object(self, queryset=None):
    #     """ Hook to ensure object is owned by request.user. """
    #     obj = super(CommentDeleteView, self).get_object()
    #     if not obj.owner == self.request.user:
    #         raise Http404
    #     return obj


class CommentListView(AjaxableResponseMixin, ListView):
    model = InternalExternalComment
    template_name = 'internal_external_comments/list.html'
    fields = '__all__'


class CommentObjectListView(ListView):
    model = InternalExternalComment
    template_name = 'internal_external_comments/list.html'
    fields = '__all__'

    def get_queryset(self):
        return InternalExternalComment.objects.filter(
            content_type__app_label=self.kwargs['app_label'],
            content_type__model=self.kwargs['model'],
            object_pk=self.kwargs['object_pk'],
        )
