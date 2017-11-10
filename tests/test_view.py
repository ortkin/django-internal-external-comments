from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.core.urlresolvers import resolve
from django.contrib.auth import get_user_model

from internal_external_comments.views import (CommentDetailView, CommentListView,
                                              CommentObjectListView, CommentCreateView)
from internal_external_comments.forms import InternalExternalCommentForm
from internal_external_comments.models import InternalExternalComment


def setup_view(view, request, *args, **kwargs):
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view


class InternalExternalViewTests(TestCase):
    def getData(self):
        return {
            'name': "Frodo Baggins",
            'email': "frodo.baggins@bagend.org",
            'comment': ("Come on, Sam. Remember what Bilbo used to say: "
                        "\"It\'s a dangerous business, Frodo, going out your door. "
                        "You step onto the road, and if you don\'t keep your feet, "
                        "there\'s no knowing where you might be swept off to.\""),
            'content_type_id': 21,
            'site_id': 1,
        }

    def getValidData(self):
        # create form for target self.user
        f = InternalExternalCommentForm(self.user)
        d = self.getData()
        d.update(f.initial)
        return d

    def setUp(self):
        self.user = get_user_model().objects.create_user('gandalf the white')
        self.factory = RequestFactory()
        self.client = Client()

    @classmethod
    def setUpTestData(cls):
        InternalExternalComment.objects.create(name="Frodo Baggins",
                                               email="frodo.baggins@bagend.org",
                                               comment=("Come on, Sam. Remember what Bilbo used to say: "
                                                        "\"It\'s a dangerous business, Frodo, going out your door. "
                                                        "You step onto the road, and if you don\'t keep your feet, "
                                                        "there\'s no knowing where you might be swept off to.\""),
                                               content_type_id=21,
                                               site_id=1,
                                               )

    def test_comment_exists(self):
        self.assertEqual(InternalExternalComment.objects.count(), 1)

    def test_view_uses_correct_template(self):
        request = RequestFactory().get(reverse('comments_urls:comments-detail', kwargs={'pk': 1}))
        view = setup_view(CommentDetailView(), request)
        self.assertEqual(view.template_name, 'internal_external_comments/comment.html')

    # def test_200_response_from_get_request(self):
    #     request = self.factory.get('/fake/')
    #     request.user = self.user
    #     view = setup_view(CommentCreateView(), request, **self.getData())
    #     print(view)
    #     view.get(request, **self.getData())
    #     self.assertEqual(view.kwargs['name'], "Frodo Baggins")

    def test_CommentListView(self):
        url = reverse('comments_urls:comments-list')
        request = RequestFactory().get(url)
        view = setup_view(CommentListView(), request)
        self.assertEqual(view.get_queryset().count(), 1)

    # def test_CommentObjectListView(self):
    #     url = reverse('comments_urls:comments-object-list',
    #                   kwargs={'app_label': 'auth', 'model': 'user', 'object_pk': 21})
    #     request = RequestFactory().get(url)
    #     print(request)
    #     view = setup_view(CommentObjectListView(), request)
    #     print(dir(view))
    #     print(view.args)
    #     print(view.kwargs)
    #     self.assertEqual(view.get_queryset().count(), 1)
    #     print(view.get_queryset())
