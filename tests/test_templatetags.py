from django.test import TestCase, RequestFactory
from django.template import Context, Template
from django.contrib.auth import get_user_model


class InternalExternalTemplateTagTests(TestCase):
    def setUp(self):
        super(InternalExternalTemplateTagTests, self).setUp()
        self.user = get_user_model().objects.create_user('gandalf the gray')
        self.request = RequestFactory().get('/fake-path')
        self.request.user = self.user

    def test_form_rendered(self):
        context = Context({'request': self.request, 'user': self.user})
        template_to_render = Template(
            '{% load comments %}'
            '{% comments_form for user %}'
        )
        rendered_template = template_to_render.render(context)
        # print(rendered_template)
        self.assertInHTML('<h1>my_title</h1>', rendered_template)


    def test_list_rendered(self):
        context = Context({'request': self.request, 'user': self.user})
        template_to_render = Template(
            '{% load internalexternal_tags %}'
            '{% comments for user as comment_list %}'
        )
        rendered_template = template_to_render.render(context)
        # print(rendered_template)
        self.assertInHTML('<h1>my_title</h1>', rendered_template)
