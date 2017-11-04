from django.test import TestCase
import django_comments as comments

from internal_external_comments.models import InternalExternalComment

try:
    import jinja2
except ImportError:
    jinja2 = None


class InternalExternalModelTests(TestCase):
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

    def test_comment_using_internal_external(self):
        cob = comments.get_model()
        self.assertEqual('InternalExternalComment', cob.__name__)

    def test_comment_verbose(self):
        cob = comments.get_model()
        self.assertEquals(cob._meta.verbose_name, 'Comment')

    def test_comment_verbose_plural(self):
        cob = comments.get_model()
        self.assertEquals(cob._meta.verbose_name_plural, 'Comments')

    def test_comment_exists(self):
        self.assertEqual(InternalExternalComment.objects.count(), 1)

    def test_is_internal(self):
        cob = comments.get_model()
        comment = cob.objects.get(id=1)
        self.assertEqual(comment.is_internal, True)
