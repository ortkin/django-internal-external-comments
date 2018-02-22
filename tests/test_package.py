from django.test import SimpleTestCase, Client
from django.apps import apps
from django.urls import reverse
from django.core.urlresolvers import resolve

from internal_external_comments import get_form, get_model, admin
from internal_external_comments.apps import CommentsAppConfig
from internal_external_comments.forms import InternalExternalCommentForm
from internal_external_comments.models import InternalExternalComment


class InternalExternalTests(SimpleTestCase):

    def test_get_model(self):
        self.assertEqual(get_model(), InternalExternalComment)

    def test_get_form(self):
        self.assertEqual(get_form(), InternalExternalCommentForm)


class InternalExternalAdmin(SimpleTestCase):
    def test_admin_exists(self):
        self.assertEqual(admin.__name__, 'internal_external_comments.admin')


class InternalExternalApps(SimpleTestCase):
    def test_apps_name(self):
        self.assertEqual(CommentsAppConfig.name, 'internal_external_comments')
        self.assertEqual(apps.get_app_config('internal_external_comments').name, 'internal_external_comments')

    def test_apps_verbose_name(self):
        self.assertEqual(CommentsAppConfig.verbose_name, 'Comments')


class InternalExternalURLTests(SimpleTestCase):
    client = Client()

    def test_list(self):
        url = reverse('comments_urls:comments-list')
        self.assertEqual(url, '/list/')

    def test_object_list(self):
        url = reverse('comments_urls:comments-object-list',
                      kwargs={'app_label': 'label', 'model': 'mymodel', 'object_pk': 1})
        self.assertEqual(url, '/listmodel/label/mymodel/1/')
