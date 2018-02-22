from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from internal_external_comments.views import (CommentObjectListView,
                                              CommentObjectCreateView, CommentDetailView)
from internal_external_comments.forms import InternalExternalCommentForm
from internal_external_comments.models import InternalExternalComment


def setup_view(view, request, *args, **kwargs):
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view


class InternalExternalViewTests(TestCase):
    def postData(self):
        return {
            'user': self.user,
            'comment': ("All you have to decide is what to do with the time that is given to you."),
            'content_type_id': ContentType.objects.get_for_model(
                self.user).pk,
            'site_id': 1,
            'object_pk': self.user.pk
        }

    def getData(self):
        return {'app_label': 'auth', 'model': 'user', 'object_pk': self.user.pk}

    def getValidData(self):
        # create form for target self.user
        f = InternalExternalCommentForm(self.user)
        d = self.getData()
        d.update(f.initial)
        return d

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.object_list_url = reverse('comments_urls:comments-object-list',
                                       kwargs={'app_label': 'auth', 'model': 'user', 'object_pk': self.user.pk})

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user('gandalf the white')
        InternalExternalComment.objects.create(name="Frodo Baggins",
                                               email="frodo.baggins@bagend.org",
                                               comment=("Come on, Sam. Remember what Bilbo used to say: "
                                                        "\"It\'s a dangerous business, Frodo, going out your door. "
                                                        "You step onto the road, and if you don\'t keep your feet, "
                                                        "there\'s no knowing where you might be swept off to.\""),
                                               content_type_id=ContentType.objects.get_for_model(
                                                   cls.user).pk,
                                               site_id=1,
                                               object_pk=cls.user.pk,
                                               )
        cls.test_comment = InternalExternalComment.objects.get(pk=1)
        InternalExternalComment.objects.create(name="Samwise Gamgee",
                                               email="samwise.gamgee@bagend.org",
                                               comment=(
                                                   "That there’s some good in this world, Mr. Frodo. And it’s worth fighting for."),
                                               content_type_id=ContentType.objects.get_for_model(
                                                   cls.test_comment).pk,
                                               site_id=1,
                                               object_pk=cls.test_comment.pk,
                                               )

    def test_comment_exists(self):
        self.assertEqual(InternalExternalComment.objects.count(), 2)

    def test_view_uses_correct_template(self):
        request = RequestFactory().get(reverse('comments_urls:comments-detail', kwargs={'pk': 1}))
        view = setup_view(CommentDetailView(), request)
        self.assertEqual(view.template_name, 'internal_external_comments/comment.html')

    def test_CommentObjectCreateView_get(self):
        request = self.factory.get(self.object_list_url)
        request.user = self.user
        view = setup_view(CommentObjectCreateView(), request, **self.getData())
        print(view.request, view.args, view.kwargs)
        response = view.dispatch(view.request, *view.args, **view.kwargs)
        print('response', response)
        self.assertEqual(view.kwargs['user'], "gandalf the white")

    def test_CommentObjectListView_view(self):
        request = RequestFactory().get(self.object_list_url)
        view = setup_view(CommentObjectListView(), request, **self.getData())
        self.assertEqual(view.get_queryset().count(), 1)
        comments = InternalExternalComment.objects.filter(
            content_type__app_label='auth',
            content_type__model='user',
            object_pk=self.user.pk,
        )
        self.assertQuerysetEqual(comments, map(repr, view.get_queryset()), ordered=False)

    def test_CommentObjectListView_integration(self):
        response = self.client.get(self.object_list_url)
        self.assertEqual(200, response.status_code)
        findstr = '<div id="comments-{}-{}"'.format(
            ContentType.objects.get_for_model(self.user), self.user.pk)
        self.assertContains(response, findstr)
        self.assertTemplateUsed(response, 'internal_external_comments/list.html')

    def test_object_list_view_uses_correct_template(self):
        request = RequestFactory().get(self.object_list_url)
        view = setup_view(CommentObjectListView(), request)
        self.assertEqual(view.template_name, 'internal_external_comments/list.html')
