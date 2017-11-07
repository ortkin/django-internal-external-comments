from django.test import TestCase
from django.contrib.auth import get_user_model

from internal_external_comments.forms import InternalExternalCommentForm


class InternalExternalFormTests(TestCase):

    def getData(self):
        return {
            'name': "Frodo Baggins",
            'email': "frodo.baggins@bagend.org",
            'comment': ("Come on, Sam. Remember what Bilbo used to say: "
                        "\"It\'s a dangerous business, Frodo, going out your door. "
                        "You step onto the road, and if you don\'t keep your feet, "
                        "there\'s no knowing where you might be swept off to.\""),
        }

    def getValidData(self):
        # create form for target self.user
        f = InternalExternalCommentForm(self.user)
        d = self.getData()
        d.update(f.initial)
        return d

    def setUp(self):
        super(InternalExternalFormTests, self).setUp()
        self.user = get_user_model().objects.create_user('gandalf the white')

    def test_form_init(self):
        f = InternalExternalCommentForm(self.user)
        self.assertEqual(f.initial['content_type'], 'auth.user')
        self.assertEqual(f.initial['object_pk'], "1")
        self.assertNotEqual(f.initial['security_hash'], None)
        self.assertNotEqual(f.initial['timestamp'], None)
        # check custom field
        self.assertEqual(f.initial['internal_external'], "internal")

    def test_form_internal_external_initial_exists(self):
        init_data = self.getData()
        init_data['internal_external'] = "external"
        f = InternalExternalCommentForm(self.user, initial=init_data)
        self.assertTrue('internal_external' in f.initial)
        self.assertEqual(init_data['internal_external'], f.initial['internal_external'])

    def test_form_internal_external_exists(self):
        f = InternalExternalCommentForm(self.user)
        self.assertTrue('internal_external' in f.initial)

    def test_valid_form(self):
        form = InternalExternalCommentForm(self.user, data=self.getValidData())
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = InternalExternalCommentForm(self.user, {})
        self.assertFalse(form.is_valid())

    def test_get_comment_model(self):
        form = InternalExternalCommentForm(self.user, self.getValidData())
        self.assertEqual(InternalExternalCommentForm, form.get_comment_model())

    def test_get_comment_object(self):
        form = InternalExternalCommentForm(self.user, self.getValidData())
        form.is_valid()
        comment = form.get_comment_object()
        self.assertTrue("internal_external" in dir(comment))

    def test_get_comment_object_invalid_form(self):
        form = InternalExternalCommentForm(self.user, {})
        try:
            form.get_comment_object()
            self.fail("get_comment_object should fail when form not valid")
        except Exception:
            pass

    def test_get_comment_create_data(self):
        form = InternalExternalCommentForm(self.user, self.getValidData())
        form.is_valid()
        data = form.get_comment_create_data()
        self.assertTrue("internal_external" in data)
        self.assertEqual(data['internal_external'], 'internal')

    def test_get_comment_create_data_external(self):
        data = self.getValidData()
        data['internal_external'] = 'external'
        form = InternalExternalCommentForm(self.user, data)
        form.is_valid()
        data = form.get_comment_create_data()
        self.assertTrue("internal_external" in data)
        self.assertEqual(data['internal_external'], 'external')

    def test_get_comment_create_data_external_none_is_internal(self):
        data = self.getValidData()
        data['internal_external'] = None
        form = InternalExternalCommentForm(self.user, data)
        form.is_valid()
        data = form.get_comment_create_data()
        self.assertTrue("internal_external" in data)
        self.assertEqual(data['internal_external'], "internal")
        widget = form.fields['comment'].widget
        self.assertEqual(widget.internal_external, "internal")

    def test_get_comment_create_data_external_external(self):
        data = self.getValidData()
        data['internal_external'] = 'external'
        form = InternalExternalCommentForm(self.user, data=data)
        form.is_valid()
        widget = form.fields['comment'].widget
        self.assertEqual(widget.internal_external, "external")
