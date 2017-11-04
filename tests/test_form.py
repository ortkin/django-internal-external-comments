from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site

from internal_external_comments.forms import InternalExternalCommentForm


try:
    import jinja2
except ImportError:
    jinja2 = None


class InternalExternalFormTests(TestCase):
    ENTRY_DATA = {
        'object_pk': 1,
        'name': "Frodo Baggins",
        'email': "frodo.baggins@bagend.org",
        'comment': ("Come on, Sam. Remember what Bilbo used to say: "
                    "\"It\'s a dangerous business, Frodo, going out your door. "
                    "You step onto the road, and if you don\'t keep your feet, "
                    "there\'s no knowing where you might be swept off to.\""),
        'internal_external': "internal"
    }
    TEST_DATA = {
        'object_pk': 1,
        'user_name': "Gandalf",
        'user_email': "gandalf@thewhite.org",
        'comment': ("A wizard is never late, Frodo Baggins. Nor is he early. "
                    "\He arrives precisely when he means to. "),
    }

    def setUp(self):
        self.user = get_user_model().objects.create_user('zoidberg')
        self.content_type = ContentType.objects.get_for_model(get_user_model())
        self.site = Site(domain="testserver", name="testserver")
        self.ENTRY_DATA['content_type'] = self.content_type
        self.ENTRY_DATA['site'] = Site.objects.get_current()
        self.form = InternalExternalCommentForm(self.user)
        self.ENTRY_DATA.update(self.form.initial)

    def test_form_init(self):
        f = InternalExternalCommentForm(self.user, data=self.ENTRY_DATA)
        self.assertEqual(f.initial['content_type'], 'auth.user')
        self.assertEqual(f.initial['object_pk'], "1")
        self.assertNotEqual(f.initial['security_hash'], None)
        self.assertNotEqual(f.initial['timestamp'], None)

    def test_valid_data(self):
        form = InternalExternalCommentForm(self.user, data=self.ENTRY_DATA)
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = InternalExternalCommentForm(self.user, {})
        self.assertFalse(form.is_valid())

    def test_get_comment_model(self):
        form = InternalExternalCommentForm(self.user, data=self.ENTRY_DATA)
        self.assertEqual(InternalExternalCommentForm, form.get_comment_model())

    def test_get_comment_object(self):
        form = InternalExternalCommentForm(self.user, data=self.ENTRY_DATA)
        form.is_valid()
        comment = form.get_comment_object()
        self.assertTrue("internal_external" in dir(comment))

    def test_get_comment_create_data(self):
        form = InternalExternalCommentForm(self.user, data=self.ENTRY_DATA)
        form.is_valid()
        data = form.get_comment_create_data()
        self.assertTrue("internal_external" in data)


class InternalExternalViewTests(TestCase):
    pass
